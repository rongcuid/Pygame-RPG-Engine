'''
Created on Sep 1, 2013

@author: carl
'''
# ----------------------------------
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
        return [charactor,sector]
    
    
    def GetMoveData(self):
        return [self.characters[0]]
    def SetGame(self,game):
        self.game = game
    def SetData(self,playerDict):
        self.name = playerDict['name']
    
    def Notify(self,event):
        pass
#---------------------------------
class Charactor:
    def __init__(self,evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.sector = None
    # --------------------
    def Move(self, direction):
        if self.sector.MovePossible(direction):
            newSector = self.sector.neighbors[direction]
            self.sector = newSector
            ev = Events.CharactorMoveEvent( self )
            self.evManager.Post( ev )
    
    #------------------------------
    def Place(self, sector):
        self.sector = sector
        ev = Events.CharactorPlaceEvent(self)
        self.evManager.Post(ev)
    
    #--------------------------
    def Notify(self,event):
        if isinstance( event, Events.GameStartedEvent ):
            gameMap = event.game.map
            self.Place(gameMap.sectors[gameMap.startSectorIndex])
        elif isinstance(event, Events.CharactorMoveRequest):
            self.Move(event.direction)