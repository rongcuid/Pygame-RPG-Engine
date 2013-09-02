'''
Created on Sep 1, 2013

@author: carl
'''

import pygame
from pygame.locals import *

import Events

from GameConstants import *

#----------------------------------
class Map:
    '''
    '''
    STATE_PREPARING = 0
    STATE_BUILT = 1
    
    # ------------------------------------------
    def __init__(self,evManager):
        self.evManager = evManager
        
        self.state = Map.STATE_PREPARING
        
        self.sectors = []
        self.startSectorIndex = 0
    
    #-----------------------------------
    def Build(self):
        for i in range(9):
            #self.sectors[i] = Sector( self.evManager )
            self.sectors.append(Sector(self.evManager))
        for i in range(3,9):
            self.sectors[i].neighbors[DIRECTION_UP] = self.sectors[i - 3]
        for i in range(0,6):
            self.sectors[i].neighbors[DIRECTION_DOWN] = self.sectors[i + 3]
        for i in [1,2,4,5,7,8]:
            self.sectors[i].neighbors[DIRECTION_LEFT] = self.sectors[i - 1]
        for i in [0,1,3,4,6,7]:
            self.sectors[i].neighbors[DIRECTION_RIGHT] = self.sectors[i + 1]
            
        self.state = Map.STATE_BUILT
        
        ev = Events.MapBuiltEvent(self)
        self.evManager.Post(ev)

# ----------------------------
class Sector:
    def __init__(self,evManager):
        self.evManager = evManager
        
        #self.neighbors = range(4)
        self.neighbors = {}
        
        self.neighbors[DIRECTION_UP] = None
        self.neighbors[DIRECTION_DOWN] = None
        self.neighbors[DIRECTION_LEFT] = None
        self.neighbors[DIRECTION_RIGHT] = None
        
    def MovePossible(self,direction):
        if self.neighbors[direction]:
            return 1
#--------------------