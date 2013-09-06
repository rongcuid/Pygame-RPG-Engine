'''
This file is the View part of the game.
Contains class PygameView
'''

import sys
import pygame
from pygame.locals import *

from Debug import Debug

import GameConstants
import EventManager
import Events
import Controllers


#---------------------------------
class PygameView:
    '''
    Pygame View of the game, handles the display
    '''
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        pygame.init()
        self.window = pygame.display.set_mode( (800,600) )
        #self.window.fill((255,255,255))
        pygame.display.set_caption( 'Test Game' )
        self.background = pygame.Surface( self.window.get_size() )
        self.background.fill( (0,255,0) )
        # Test
        font = pygame.font.Font(None, 30)
        text = "Test Text"
        textImg = font.render( text, 1, (255,0,0))
        self.background.blit( textImg,(0,0) )

        #testTilesetImg = pygame.image.load('data/test1_tileset.png')
        #testTile = testTilesetImg.subsurface(0,0,32,32)
        #self.background.blit( testTile, (0,0) )
        #-----------

        self.window.blit(self.background,(0,0))
        pygame.display.flip()
        
        self.overlays = pygame.sprite.RenderUpdates()
    #-------------------------------
    def ShowMap(self, gameMap, xoffset=0,yoffset=0):
        # Clear screen
        mapLayers = gameMap.layers
        self.background.fill((0,0,0))
        self.window.blit( self.background,(0,0))
        pygame.display.flip()

        #mapLayer = mapLayers[0] # test code

        # Draw objects
        for mapLayer in mapLayers:
            for tile_y in range(0,len(mapLayer)):
                for tile_x in range(0,len(mapLayer[0])):
                    self.DrawTile(tile_x,tile_y,mapLayer)
       # Test code
        #overlay = pygame.sprite.Sprite(self.overlays)
        #testTile = mapLayer[2][1]
        #overlay.image = testTile
        #overlay.rect = testTile.get_rect().move(16,16)
        # -----------
        self.window.blit(self.background,(0,0))
        self.overlays.draw(self.window)
        pygame.display.flip()

    #-----------------------------
    def DrawTile(self,tile_x,tile_y,mapLayer):
        tile = mapLayer[tile_y][tile_x]
        if tile: # Makes sure the tile is not None
            overlay = pygame.sprite.Sprite(self.overlays)
            overlay.image = tile
            overlay.rect = tile.get_rect().move(
                    tile_x * GameConstants.TILESIZE,
                    tile_y * GameConstants.TILESIZE)
 
    #-------------------------------
    def Notify(self,event):
        if isinstance( event, Events.TickEvent ):
            pygame.display.update()
        elif isinstance( event, Events.MapBuiltEvent):
            gameMap = event.map
            self.ShowMap(gameMap)


