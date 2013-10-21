'''
This file is the View part of the game.
Contains class PygameView
'''

import sys
import pygame
from pygame.locals import *

from Debug import Debug

import GameConstants as GC
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
        self.current_map = None
        self.game = None
        self.messages = []
        # -----------------
        pygame.init()

        pygame.key.set_repeat(GC.KEY_REPEAT_DELAY,
                GC.KEY_REPEAT_INTERVAL)
        self.window = pygame.display.set_mode(GC.WINDOWSIZE)
        pygame.display.set_caption('Core Engine')
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 0, 0))

        self.window.blit(self.background, (0, 0))
        pygame.display.update()

        self.backSprite = pygame.sprite.RenderUpdates()
        self.frontSprite = pygame.sprite.RenderUpdates()

        self.map_layer = pygame.sprite.Sprite(self.backSprite)
        self.charactor_layer = pygame.sprite.Sprite(self.frontSprite)

    #-------------------------------

    #def ShowMap(self, gameMap):
    def PrepMap(self, gameMap):
        self.state = PygameView.STATE_MAP_BUILDING
        mapLayers = gameMap.GetLayers()
        tiles = self.DrawTile(mapLayers)
        map_img = pygame.Surface((tiles.get_rect().w,tiles.get_rect().h))
        map_img.blit(tiles, (0,0))
        self.state = PygameView.STATE_IDLE
        return map_img

    def ShowMap(self, map_img):
        self.map_layer.image = map_img
        self.map_layer.rect = \
                self.map_layer.image.get_rect().move(
                        self.xoffset - GC.TILESET_TILESIZE / 2,
                        self.yoffset - GC.TILESET_TILESIZE / 2)


    #-----------------------------
    def ShowCharactor(self, charactor):
        # TODO: Overlaid charactor sprite
        # TODO: Animation etc
        sector = charactor.sector
        sprite = charactor.sprite

        if self.camera_state == PygameView.CAMERA_TRACK_DISABLED:
            sprite.moveTo = (sector.x * GC.TILESIZE + self.xoffset - GC.TILESIZE / 2,
                    sector.y * GC.TILESIZE + self.yoffset - GC.TILESIZE / 2)
        #elif self.camera_state == PygameView.CAMERA_TRACK_ENABLED \
                #    and self.trackto == charactor:

        elif self.trackto == charactor:
            sprite.moveTo = (GC.WINDOWSIZE[0] / 2 - GC.TILESIZE / 2,
                            GC.WINDOWSIZE[1] / 2 - GC.TILESIZE / 2)
            self.UpdateCameraOffset(GC.WINDOWSIZE[0] / 2 - sector.x * GC.TILESIZE,
                            GC.WINDOWSIZE[1] / 2 - sector.y * GC.TILESIZE)

        self.charactor_layer.image = sprite.image 
        self.charactor_layer.rect = sprite.rect 
        #----------------
    def DrawTile(self, mapLayers):
        max_w = 0
        max_h = 0
        for l in mapLayers:
            if len(l) > max_h:
                max_h = len(l)
            if len(l[0]) > max_w:
                max_w = len(l[0])
        size = (max_w * GC.TILESIZE,
                max_h * GC.TILESIZE)
        image = pygame.Surface(size)
        for mapLayer in mapLayers:
            for tile_y in range(0, len(mapLayer)):
                for tile_x in range(0, len(mapLayer[0])):
                    tile = mapLayer[tile_y][tile_x]
                    if tile:
                        self.DrawOneTile(image, tile,
                                tile_x, tile_y)
        return image

    #-------------------
    def DrawOneTile(self, image, tile, tile_x, tile_y):
        if tile:
            image.blit(tile,
                    (tile_x * GC.TILESIZE,
                    tile_y * GC.TILESIZE))


    #------------------------------
    def UpdateCameraOffset(self, xoffset = None, yoffset = None):
        if xoffset != None:
            self.xoffset = xoffset
        if yoffset != None:
            self.yoffset = yoffset

    def SetTrack(self, charactor):
        self.trackto = charactor
        self.camera_state = PygameView.CAMERA_TRACK_ENABLED

    def DisableTrack(self):
        self.trackto = None
        self.camera_state = PygameView.CAMERA_TRACK_DISABLED

    def Notify(self, event):
        if isinstance(event, Events.GameStartedEvent):
            self.game = event.game
        elif isinstance(event, Events.LogicTickEvent):
            self.frames += 1
            if self.state == self.STATE_IDLE:
                for charactor in self.game.charactors:
                    self.ShowCharactor(charactor)
                self.ShowMap(self.current_map)

                self.backSprite.update()
                self.frontSprite.update()

                self.backSprite.clear(self.window,self.background)
                self.frontSprite.clear(self.window,self.background)

                dirtyRect1 = self.backSprite.draw(self.window)
                dirtyRect2 = self.frontSprite.draw(self.window)
                dirtyRects = dirtyRect1 + dirtyRect2

                pygame.display.update(dirtyRects)
        elif isinstance(event, Events.SecondEvent):
            if GC.SHOW_FPS:
                Debug("PygameView: FPS = ", self.frames)
            self.frames = 0

        elif isinstance(event, Events.MapBuiltEvent):
            self.gameMaps.append(event.map)
            # Test Code
            self.current_map = self.PrepMap(event.map)
            # ----------
        # Test
        elif isinstance(event, Events.KeyPressedEvent):
            if event.key == K_t:
                if self.camera_state == PygameView.CAMERA_TRACK_DISABLED:
                    self.SetTrack(self.game.charactors[0])
                    Debug("Track enabled")
                else:
                    self.DisableTrack()
                    Debug("Track disabled")
        #---
        elif isinstance(event, Events.WindowResizeRequest):
            pygame.display.quit()
            pygame.display.init()
            self.window = pygame.display.set_mode(event.size)
            self.background = pygame.Surface(self.window.get_size())
            self.background.fill((0, 0, 0))

            self.window.blit(self.background, (0, 0))
            pygame.display.update()
