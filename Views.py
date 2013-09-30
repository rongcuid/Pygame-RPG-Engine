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
    STATE_MAP_BUILDING = 0
    STATE_IDLE = 1

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.state = self.STATE_IDLE

        self.frames = 0

        pygame.init()

        pygame.key.set_repeat(100,100)
        self.window = pygame.display.set_mode(GameConstants.WINDOWSIZE)
        # self.window.fill((255,255,255))
        pygame.display.set_caption('Test Game')
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 0, 0))
        #-----------

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        self.backSprite = pygame.sprite.RenderUpdates()

    #-------------------------------

    def ShowMap(self, gameMap, xoffset=0, yoffset=0):
        # TODO: Offsets, or Camera
        # Clear screen
        self.state = self.STATE_MAP_BUILDING
        mapLayers = gameMap.GetLayers()
        self.background.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        # Draw objects
        map_img = self.DrawTile(mapLayers)
        overlay = pygame.sprite.Sprite(self.backSprite)
        overlay.image = map_img
        overlay.rect = map_img.get_rect()

        self.window.blit(self.background, (0, 0))
        self.backSprite.draw(self.window)
        pygame.display.flip()
        self.state = self.STATE_IDLE

    #-----------------------------
    def ShowCharactor(self, charactor):
        # TODO: Overlaid charactor sprite
        sector = charactor.sector
        sprite = charactor.sprite
        #self.background.blit(sprite.image,sprite.rect.topleft)
        #self.window.blit(self.background,(0,0))
        
    def DrawTile(self, mapLayers):
        #tile = mapLayer[tile_y][tile_x]
        #if tile:  # Makes sure the tile is not None
        #    self.background.blit(
        #        tile, (tile_x * GameConstants.TILESIZE,
        #                tile_y * GameConstants.TILESIZE))
        image = pygame.Surface(self.window.get_size())
        for mapLayer in mapLayers:
            for tile_y in range(0, len(mapLayer)):
                for tile_x in range(0, len(mapLayer[0])):
                    tile = mapLayer[tile_y][tile_x]
                    if tile:
                        self.DrawOneTile(image, tile,
                                tile_x, tile_y)
        #self.background.blit(image,(0,0))
        return image
    def DrawOneTile(self, image, tile, tile_x, tile_y):
        if tile:
            image.blit(tile,
                    (tile_x * GameConstants.TILESIZE,
                    tile_y * GameConstants.TILESIZE))


    #------------------------------
    def Notify(self, event):
        if isinstance(event, Events.TickEvent):
            if self.state == self.STATE_IDLE:
                self.frames += 1
                pygame.display.flip()
        elif isinstance(event, Events.LogicTickEvent):
            #for charactor in event.game.charactors:
            #    self.ShowCharactor(charactor)
            pass
        elif isinstance(event, Events.SecondEvent):
            if GameConstants.SHOW_FPS:
                Debug("PygameView: FPS = ", self.frames)
            self.frames = 0
        elif isinstance(event, Events.MapBuiltEvent):
            gameMap = event.map
            self.ShowMap(gameMap)
