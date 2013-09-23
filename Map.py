'''
Created on Sep 1, 2013

@author: carl
'''

import sys
import traceback
import json
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
        self.evManager.RegisterListener(self)

        self.state = Map.STATE_PREPARING

        tileLayersData, tilesetsData = self.Read('data/test1-3x3.json')
        self.tileList,self.tileProp = self.LoadTileList(tilesetsData)

        # This is used to store layers built
        self.layers = []

        for l in range(len(tileLayersData)):
            self.layers.append(
                self.Build(tileLayersData[l]['data'],
                           tileLayersData[l]['width']))  



        self.state = Map.STATE_BUILT
        evManager.Post(Events.MapBuiltEvent(self))
    #-----------------------
    def GetLayers(self):
        layers = []
        for l in self.layers:
            layers.append(l[0])
        return layers
    #-----------------------
    def GetLayerProps(self):
        props = []
        for l in self.layers:
            props.append(l[1])
        return props
    #-----------------------

    def Read(self, filename):
        '''
        This function reads map data from a Json file
        @return: [tileLayersData,tilesetsData]
        '''
        try:
            map_data = json.load(open(filename))
        except:
            raise Exception("Error: Cannot read map data file ", filename)
        Debug("Map data ", filename, " is successfully read!")
        tileLayersData = map_data['layers']
        tilesetsData = map_data['tilesets']

        return [tileLayersData, tilesetsData]
    #-----------------------

    def Build(self, tileMapData, columns):
        '''
        Reads a list of tiles used, the number of 
        columns of tiles for the width, and construct map
        '''
        rows = int(len(tileMapData) / columns)
        tileMap = []
        tilePropMap = []
        for tile_row in range(0, rows):
            tileMap.append([])
            tilePropMap.append([])
            for tile_column in range(0, columns):
                # Retrieve tile address in tileset from tileMapData, read the tile from tileList,
                # then assign that to the corresponding entry in tileMap
                tileMap[tile_row].append(
                    self.tileList[
                        tileMapData[tile_row * columns + tile_column] - 1])
                # Retrieve tile address in tileset from tileMapData, read property from tileProp,
                # then assign that to corresponding entry in tilePropMap
                tilePropMap[tile_row].append(
                        self.tileProp[
                            tileMapData[tile_row * columns + tile_column] - 1])
        Debug("Tile map initialized")
        return [tileMap,tilePropMap]
    #-----------------------

    def LoadTileList(self, tilesets):
        '''
        Loads tile list from tileset. 
        Iterates through tilesets to make tile lists
        from different tilesets. Key of tileList
        includes the offset of tileset
        '''
        # A dict of tiles available
        tileList = {}
        # A dict of tile properties
        tileProp = {}
        for tilesetData in tilesets:
            try:
                tilesetImg = pygame.image.load('data/' + tilesetData['image'])
            except:
                raise Exception(
                    "Error: Tile set file \'", tilesetData['image'], "\' does not exist.")
            Debug("Tileset image is successfully loaded")
            tilesetWidth, tilesetHeight = tilesetImg.get_size()
            # This is the index offset of tileset
            count = tilesetData['firstgid'] - 1
            for tile_y in range(0,
                                int(tilesetHeight / GameConstants.TILESET_TILESIZE)):
                for tile_x in range(0,
                                    int(tilesetWidth / GameConstants.TILESET_TILESIZE)):
                    rect = (tile_x * GameConstants.TILESET_TILESIZE,
                            tile_y * GameConstants.TILESET_TILESIZE,
                            GameConstants.TILESIZE, GameConstants.TILESIZE)
                    tileList[count] = tilesetImg.subsurface(rect)
                    tileProp[count] = tilesetData['properties']
                    count += 1
            # When there is no tile, i.e. tile data is 0
            tileList[-1] = None
            Debug("Tileset list is successfully created")
            tileProp[-1] = None
            Debug("Tileset property is successfully created")
        return [tileList,tileProp]

    #-----------------------
    def Notify(self, event):
        '''
        NOTE: should use imported event lists for levels
        '''
        pass
#--------------------------


class Tile:

    def __init__(self, evManager, surface=None):
        '''
        Initiates a tile. Can have surface to display
        '''
        self.evManager = evManager
