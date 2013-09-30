'''
Created on Sep 1, 2013

@author: carl
'''
# ----------------------------------

from pygame.locals import *
import GameConstants
import Events
from Debug import Debug

class Player:

    def __init__(self, evManager):
        self.evManager = evManager
        self.game = None
        self.name = ""
        self.evManager.RegisterListener(self)
        self.charactors = [Charactor(evManager)]

    def __str__(self):
        return '<Player %s %s>' % (self.name, id(self))

    def GetPlaceData(self):
        charactor = self.charactors[0]
        gameMap = self.game.map
        sector = gameMap.scetors[gameMap.startSectorIndex]
        return [charactor, sector]

    def GetMoveData(self):
        return [self.characters[0]]

    def SetGame(self, game):
        self.game = game

    def SetData(self, playerDict):
        self.name = playerDict['name']

    def Notify(self, event):
        pass
#---------------------------------


class Charactor:
    last_id = 0
    def __str__(self):
        return "Charactor ID " + str(self.identity) + \
                " at coordinate " + str(self.coordinate)
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        # This is a tile data
        self.sector = None
        # This is the coordinate
        self.coordinate = (None, None)
        # Set ID
        # TODO: Will be replaced by RNA
        Charactor.last_id += 1
        self.identity = Charactor.last_id
    # --------------------

    def Move(self, direction, facing=None):
        if not facing:
            facing = direction
        if self.sector.CanMove(direction):
           newSector = self.sector.neighbors[direction]
           Debug(newSector)
           self.sector = newSector
           self.UpdateCoordinate()
           ev = Events.CharactorMoveEvent(self)
           self.evManager.Post(ev)

    #------------------------------
    def Place(self, sector, facing=GameConstants.DIRECTION_UP):
        self.sector = sector
        self.UpdateCoordinate()
        ev = Events.CharactorPlaceEvent(self)
        self.evManager.Post(ev)

    def UpdateCoordinate(self):
        self.coordinate = (self.sector.x, self.sector.y)
    #--------------------------
    def Notify(self, event):
        if isinstance(event, Events.GameStartedEvent):
           gameMap = event.game.map
           #self.Place(gameMap.sectors[gameMap.startSectorIndex])
           self.Place(gameMap.sectors[0][0])
        elif isinstance(event, Events.CharactorMoveRequest):
           self.Move(event.direction)
        elif isinstance(event, Events.KeyPressedEvent):
            # TODO: If GUI is on, don't move
            # TODO: Record previous direction to change direction
            # when another key is pressed when holding the current
            # one
            if event.key == K_RIGHT:
                ev = self.Move(GameConstants.DIRECTION_RIGHT)
            elif event.key == K_LEFT:
                ev = self.Move(GameConstants.DIRECTION_LEFT)
            elif event.key == K_UP:
                ev = self.Move(GameConstants.DIRECTION_UP)
            elif event.key == K_DOWN:
                ev = self.Move(GameConstants.DIRECTION_DOWN)
