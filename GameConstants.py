'''
Created on Aug 31, 2013

This file stores all global constants in the game

@author: carl
'''

DEBUG = True
SHOW_FPS = True

LOGICRATE = 100  # Rate of logic calculation and screen refresh

WINDOWSIZE = (800, 600)

DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

TILESIZE = 32  # Width and Height of tile
# TODO: Read from json map file
TILESET_TILESIZE = 32  # Width/Height if a tile in tileset
TILESET_SPACING = 1  # Spacing between tiles

TEST_LEVEL_MAP = 'data/desert.json'

KEY_REPEAT_DELAY = 25
KEY_REPEAT_INTERVAL = 75
