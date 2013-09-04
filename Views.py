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
    def ShowMap(self, gameMap):
        # Clear screen
        self.background.fill((0,0,0))
        self.window.blit( self.background,(0,0))
        pygame.display.flip()

        mapLayer = gameMap[0]

        # Draw objects
        for tile_y in range(0,len(mapLayer)):
            for tile_x in range(0,len(mapLayer[0])):
                tile = mapLayer[tile_y][tile_x]
                overlay = pygame.sprite.Sprite(self.overlays)
                overlay.image = tile
                # NOTE: mapLayer is in form [tile_row][tile_column]
                # so tile_y goes first
                overlay.rect = tile.get_rect().move(
                        tile_y * GameConstants.TILESIZE,
                        tile_x * GameConstants.TILESIZE)
        # Test code
        #overlay = pygame.sprite.Sprite(self.overlays)
        #testTile = mapLayer[2][1]
        #overlay.image = testTile
        #overlay.rect = testTile.get_rect().move(16,16)
        # -----------
        self.window.blit(self.background,(0,0))
        self.overlays.draw(self.window)
        pygame.display.flip()

    #-------------------------------
    def Notify(self,event):
        if isinstance( event, Events.TickEvent ):
            pygame.display.update()
        elif isinstance( event, Events.MapBuiltEvent):
            gameMap = event.map
            self.ShowMap(gameMap)


