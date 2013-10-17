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

    CAMERA_TRACK_DISABLED = 0
    CAMERA_TRACK_ENABLED = 1

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        # Initialize variables/flags
        self.state = PygameView.STATE_IDLE
        self.camera_state = PygameView.CAMERA_TRACK_DISABLED
        self.frames = 0
        self.xoffset = 0
        self.yoffset = 0
        self.trackto = None
        self.gameMaps = []
        self.map_img = None
        # -----------------
        pygame.init()

        pygame.key.set_repeat(GameConstants.KEY_REPEAT_DELAY,
                GameConstants.KEY_REPEAT_INTERVAL)
        self.window = pygame.display.set_mode(GameConstants.WINDOWSIZE)
        # self.window.fill((255,255,255))
        pygame.display.set_caption('Test Game')
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 0, 0))
        #-----------

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        self.backSprite = pygame.sprite.RenderUpdates()
        self.frontSprite = pygame.sprite.RenderUpdates()

    #-------------------------------

    def ShowMap(self, gameMap):
        # TODO: Offsets, or Camera
        self.state = PygameView.STATE_MAP_BUILDING
        mapLayers = gameMap.GetLayers()
        # Test code
        if not self.map_img:
            # Draw objects
            self.map_img = self.DrawTile(mapLayers)
        overlay = pygame.sprite.Sprite(self.backSprite)
        overlay.image = self.map_img
        overlay.rect = self.map_img.get_rect().center = self.xoffset, self.yoffset

        self.state = PygameView.STATE_IDLE

    #-----------------------------
    def ShowCharactor(self, charactor):
        # TODO: Overlaid charactor sprite
        # TODO: Animation etc
        sector = charactor.sector
        sprite = charactor.sprite
        # Note: No Camera yet
        if self.camera_state == PygameView.CAMERA_TRACK_DISABLED:
            sprite.moveTo = (sector.x * GameConstants.TILESIZE + self.xoffset,
                    sector.y * GameConstants.TILESIZE + self.yoffset)
        elif self.camera_state == PygameView.CAMERA_TRACK_ENABLED and \
                self.trackto == charactor:
                    sprite.moveTo = (GameConstants.WINDOWSIZE[0] / 2 - GameConstants.TILESIZE / 2,
                            GameConstants.WINDOWSIZE[1] / 2 + GameConstants.TILESIZE / 2)
                    self.UpdateCameraOffset(GameConstants.WINDOWSIZE[0] / 2 - sector.x * GameConstants.TILESIZE,
                            GameConstants.WINDOWSIZE[1] / 2 + sector.y * GameConstants.TILESIZE)

        overlay = pygame.sprite.Sprite(self.frontSprite)
        overlay.image = sprite.image
        overlay.rect = sprite.rect
        
        #----------------
    def DrawTile(self, mapLayers):
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

    #-------------------
    def DrawOneTile(self, image, tile, tile_x, tile_y):
        if tile:
            image.blit(tile,
                    (tile_x * GameConstants.TILESIZE,
                    tile_y * GameConstants.TILESIZE))


    #------------------------------
    def UpdateCameraOffset(self, xoffset = None, yoffset = None):
        if xoffset:
            self.xoffset = xoffset
        if yoffset:
            self.yoffset = yoffset

    def SetTrack(self, charactor):
        self.trackto = charactor
        self.camera_state = PygameView.CAMERA_TRACK_ENABLED

    def DisableTrack(self):
        self.trackto = None
        self.camera_state = PygameView.CAMERA_TRACK_DISABLED

    def Notify(self, event):
        if isinstance(event, Events.LogicTickEvent):
            self.frames += 1
            if self.state == self.STATE_IDLE:
                for charactor in event.game.charactors:
                    self.ShowCharactor(charactor)
                self.ShowMap(self.gameMaps[0])
                self.backSprite.clear(self.window,self.background)
                self.frontSprite.clear(self.window,self.background)
                self.backSprite.update()
                self.frontSprite.update()

                dirtyRect1 = self.backSprite.draw(self.window)
                dirtyRect2 = self.frontSprite.draw(self.window)
                dirtyRects = dirtyRect1 + dirtyRect2
                pygame.display.update(dirtyRects)
        elif isinstance(event, Events.SecondEvent):
            if GameConstants.SHOW_FPS:
                Debug("PygameView: FPS = ", self.frames)
            self.frames = 0
            # Test Code
            self.UpdateCameraOffset(self.xoffset + 16, self.yoffset + 16)
            #-----------
        elif isinstance(event, Events.MapBuiltEvent):
            self.gameMaps.append(event.map)
