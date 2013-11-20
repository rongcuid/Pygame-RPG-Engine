'''
Created on Sep 1, 2013

@author: carl
'''

import sys
import json
import pygame
from pygame.locals import *

from Imports.common import *

import EventManager

#-----------------------------


class Map():
    STATE_PREPARING = 'Preparing'
    STATE_BUILT = 'Built'

    def __init__(self, map_file, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.map_file = map_file

        # This is used to store layers built
        self.layers = []
        self.size = (0,0)
        self.sectors = None

        self.state = None

        #self.Build()

    def Build(self):
        self.state = Map.STATE_PREPARING

        tileLayersData, tilesetsData = self.Read(self.map_file)
        self.tileList, self.tileProp = self.LoadTileSet(tilesetsData)

        self.size = (tileLayersData[0]['width'], tileLayersData[0]['height'])

        for l in range(len(tileLayersData)):
            self.layers.append(
                self.BuildLayer(tileLayersData[l]))

        self.sectors = self.SetupSectors(self.layers)

        self.state = Map.STATE_BUILT
        self.evManager.Post(Events.MapBuiltEvent(self))

    def GetLayers(self):
        layers = []
        for l in self.layers:
            layers.append(l[0])
        return layers

    def GetLayerProps(self):
        props = []
        for l in self.layers:
            props.append(l[1])
        return props

    def Read(self, filename):
        '''
        This function reads map data from a Json file
        @return: [tileLayersData,tilesetsData]
        '''
        try:
            map_data = json.load(open(filename))
        except:
            ErrorMsg("Cannot read map data file ", filename)
            raise Exception("Error: Cannot read map data file ", filename)
        Debug("Map data ", filename, " is successfully read!")
        tileLayersData = map_data['layers']
        tilesetsData = map_data['tilesets']

        return [tileLayersData, tilesetsData]

    def BuildLayer(self, tileMapData):
        '''
        Reads a list of tiles used, the number of 
        columns of tiles for the width, and construct map
        '''
        data = tileMapData['data']
        columns = tileMapData['width']
        alpha = int(tileMapData['opacity'] * 256)
        rows = int(len(data) / columns)
        assert rows * columns == len(data)  # Make sure number is correct
        tileMap = []
        tilePropMap = []
        for tile_row in range(0, rows):
            tileMap.append([])
            tilePropMap.append([])
            for tile_column in range(0, columns):
                # Initialize lists
                tileMap[tile_row].append([])
                tilePropMap[tile_row].append([])
                # Retrieve tile address in tileset from data, read the tile from tileList,
                # then assign that to the corresponding entry in tileMap
                tileMap[tile_row][tile_column] = self.tileList[
                    data[tile_row * columns + tile_column] - 1]
                if tileMap[tile_row][tile_column] != None:
                    tileMap[tile_row][tile_column].set_alpha(alpha)
                # Retrieve tile address in tileset from data, read property from tileProp,
                # then assign that to corresponding entry in tilePropMap
                tilePropMap[tile_row][tile_column] = self.tileProp[
                    data[tile_row * columns + tile_column] - 1]
        Debug("Tile map initialized")
        return [tileMap, tilePropMap]

    def LoadTileSet(self, tilesets):
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
                # TODO: Need to get rid of pygame
                tilesetImg = pygame.image.load('data/' + tilesetData['image'])
            except:
                ErrorMsg("Tile set file \'", tilesetData['image'],
                        "\' does not exist.")
                raise Exception(
                    "Error: Tile set file \'", tilesetData['image'], "\' does not exist.")
            tilesetImg = tilesetImg.convert()
            Debug("Tileset image is successfully loaded")
            spacing = tilesetData['spacing']
            margin = tilesetData['margin']
            tileset_tilesize = tilesetData['tilewidth']
            tilesetWidth, tilesetHeight = tilesetImg.get_size()
            # This is the index offset of tileset
            offset = tilesetData['firstgid'] - 1
            count = offset 
            for tile_y in range(0,
                                int(tilesetHeight / tileset_tilesize)):
                for tile_x in range(0,
                                    int(tilesetWidth / tileset_tilesize)):
                    rect = (
                        tile_x * tileset_tilesize +
                        (tile_x + margin) * spacing,
                        tile_y * tileset_tilesize +
                        (tile_y + margin) * spacing,
                        tileset_tilesize, tileset_tilesize)
                    tileList[count] = tilesetImg.subsurface(rect)
                    tileProp[count] = tilesetData.get('properties').copy()
                    addProps = tilesetData.get('tileproperties')
                    if addProps:
                        perTileProps = addProps.get(str(count - offset))
                        if perTileProps:
                            tileProp[count].update(perTileProps)
                    count += 1
            # When there is no tile, i.e. tile data is 0
            tileList[-1] = None
            Debug("Tileset list is successfully created")
            tileProp[-1] = None
            Debug("Tileset property is successfully created")
        return [tileList, tileProp]

    def SetupSectors(self, layers):
        sectors = list(range(self.size[0]))
        for s in range(len(sectors)):
            sectors[s] = list(range(self.size[1]))
        for row in range(self.size[1]):
            for col in range(self.size[0]):
                sectors[col][row] = Sector(self.evManager)

        for col in range(len(sectors)):
            for row in range(len(sectors[0])):
                # Set Properties
                prop = []
                for l in layers:
                    # Note: row and col is different
                    prop.append(l[1][row][col])
                # Set Neighbors
                up = None
                down = None
                left = None
                right = None
                if row == 0:
                    up = None
                else:
                    up = sectors[col][row - 1]
                try:
                    # When IndexError occur, sector is out of map
                    down = sectors[col][row + 1]
                except IndexError:
                    down = None
                if col == 0:
                    left = None
                else:
                    left = sectors[col - 1][row]
                try:
                    right = sectors[col + 1][row]
                except IndexError:
                    right = None
                sectors[col][row].SetNeighbors([up, down, left, right])
                sectors[col][row].SetProperties(prop)
                sectors[col][row].SetCoordinate(col,row)
        return sectors

    def Notify(self, event):
        '''
        NOTE: should use imported event lists for levels
        '''
        pass


class Sector:

    '''
    A sector stores some information of a certain tile,
    including but not limited to:
    neighbor sectors, properties
    '''

    def __str__(self):
        return "Position: " + str((self.x,self.y)) + \
                " Properties: " + str(self.properties)

    def __init__(self, evManager):
        '''
        Initiates a sector
        '''
        self.evManager = evManager
        self.neighbors = list(range(4))
        self.neighbors[GC.DIRECTION_UP] = None
        self.neighbors[GC.DIRECTION_DOWN] = None
        self.neighbors[GC.DIRECTION_LEFT] = None
        self.neighbors[GC.DIRECTION_RIGHT] = None

        self.properties = {}
        self.changed = [] # Stores changed properties

    def SetCoordinate(self, x, y):
        self.x = x
        self.y = y
    def SetNeighbors(self, neighbors=[None, None, None, None]):
        '''
        Set the neighbor sectors.
        @type neighbors: List, [UP,DOWN,LEFT,RIGHT]
        '''
        self.neighbors = list(neighbors)  # Copy the list

    def SetNeighbor(self, neighbor, direction):
        '''
        Set neighbor on one direction
        '''
        self.neighbors[direction] = neighbor

    def SetProperties(self, properties):
        '''
        Sets the properties
        @type properties: List
        '''
        if properties != None:
            for prop in properties:
                if prop != None:
                    self.properties.update(prop)

    def ChangeProperty(self, prop, val):
        self.properties[prop] = val
        self.changed.append(prop)

    def CanMove(self, direction):
        return self.neighbors[direction] != None and \
            self.neighbors[direction].properties.get('Obstacle') != 'True'
