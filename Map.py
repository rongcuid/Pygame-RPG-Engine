'''
Created on Sep 1, 2013

@author: carl
'''

import sys
import pygame
from pygame.locals import *

from Debug import Debug

import GameConstants
import EventManager
import Events

#-----------------------------
class Map():
    STATE_PREPARING = 'Preparing'
    STATE_BUILT = 'Built'
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )
        
        self.state = Map.STATE_PREPARING

        self.tileList = []
        self.LoadTileList('data/test1_tileset.png')
    #-----------------------
    def Build(self):
        # TODO: Basic builds
        pass
    #-----------------------
    def CanMove(self, tileX, tileY, direction):
        '''
        @return: Returns if charactor can move in certain
        direction on tile (tileX,tileY)
        '''
        # TODO: Implement this
        pass
    #-----------------------
    def LoadTileList(self, filename):
        '''
        Loads tile list from tileset
        '''
        try:
            tilesetImg = pygame.image.load(filename)
        except:
            print("Error: Tile set file ",filename,"does not exist.")
            pygame.quit()
            sys.exit()
        Debug("Tileset is successfully loaded")
        tilesetWidth,tilesetHeight = tilesetImg.get_size()
        for tile_y in range(0,
                int(tilesetHeight/GameConstants.TILESET_TILESIZE)):
            for tile_x in range(0,
                    int(tilesetWidth / GameConstants.TILESET_TILESIZE)):
                rect = (tile_x * GameConstants.TILESET_TILESIZE,
                        tile_y * GameConstants.TILESET_TILESIZE,
                        GameConstants.TILESIZE,GameConstants.TILESIZE)
                self.tileList.append(tilesetImg.subsurface(rect))
        Debug("Tileset list is successfully created")

    #-----------------------
    def Notify(self,event):
        '''
        NOTE: should use imported event lists for levels
        '''
        pass

#--------------------------
class Tile:
    def __init__(self,evManager,surface=None):
        '''
        Initiates a tile. Can have surface to display
        '''
        self.evManager = evManager
