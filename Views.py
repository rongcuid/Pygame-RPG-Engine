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
        self.evManager.RegisterListener(self)

        pygame.init()
        self.window = pygame.display.set_mode((800, 600))
        # self.window.fill((255,255,255))
        pygame.display.set_caption('Test Game')
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 0, 0))
        #-----------

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        self.overlays = pygame.sprite.RenderUpdates()
    #-------------------------------

    def ShowMap(self, gameMap, xoffset=0, yoffset=0):
        # TODO: Offsets, or Camera
        # Clear screen
        mapLayers = gameMap.GetLayers()
        self.background.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        # Draw objects
        for mapLayer in mapLayers:
            for tile_y in range(0, len(mapLayer)):
                for tile_x in range(0, len(mapLayer[0])):
                    self.DrawTile(tile_x, tile_y, mapLayer)
        self.window.blit(self.background, (0, 0))
        self.overlays.draw(self.window)
        pygame.display.flip()

    #-----------------------------
    def DrawTile(self, tile_x, tile_y, mapLayer):
        tile = mapLayer[tile_y][tile_x]
        if tile:  # Makes sure the tile is not None
            overlay = pygame.sprite.Sprite(self.overlays)
            overlay.image = tile
            overlay.rect = tile.get_rect().move(
                tile_x * GameConstants.TILESIZE,
                tile_y * GameConstants.TILESIZE)

    #-------------------------------
    def Notify(self, event):
        if isinstance(event, Events.TickEvent):
            pygame.display.update()
        elif isinstance(event, Events.MapBuiltEvent):
            gameMap = event.map
            self.ShowMap(gameMap)
