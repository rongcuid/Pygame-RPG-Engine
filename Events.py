'''
Created on Aug 31, 2013

This file contains all types of events in the game

@author: carl
'''

class Event():
    '''
    Superclass of all events
    '''
    def __init__(self):
        self.name = "Generic Event"
    def __str__(self):
        return '<%s %s>' % (self.__class__.__name__,id(self))
    
class TickEvent(Event):
    def __init__(self):
        self.name = "CPU Tick Event"
        
class SecondEvent(Event):
    def __init__(self):
        self.name = "Clock One Second Event"

class LogicTickEvent(Event):
    def __init__(self):
        self.name = "Logic Tick Event"

class QuitEvent(Event):
    def __init__(self):
        self.name = "Quit Event"
        
class FatalEvent(Event):
    def __init__(self):
        self.name = "Fatal Error Event"

class MapBuiltEvent(Event):
    def __init__(self,map):
        self.name = "Map Built Event"
        self.map = map
       
class GameStartRequest(Event):
    def __init__(self):
        self.name = "Game Start Request"

class GameStartedEvent(Event):
    def __init__(self,game):
        self.name = "Game Started Event"
        self.game = game

class CharactorMoveRequest(Event):
    def __init__(self, player, charactor, direction):
        self.name = "Charactor Move Request"
        self.player = player
        self.charactor = charactor
        self.direction = direction

class CharactorMoveEvent(Event):
    def __init__(self,charactor):
        self.name = "Charactor Move Event"
        self.charactor = charactor

class CharactorPlaceRequest(Event):
    def __init__(self, player, charactor, sector):
        self.name = "Charactor Placement Request"
        self.player = player
        self.charactor = charactor
        self.sector = sector

class CharactorPlaceEvent(Event):
    '''
    Placing a charactor at certain point
    '''
    def __init__(self, charactor):
        self.name = "Charactor Place Event"
        self.charactor = charactor

class PlayerJoinEvent(Event):
    def __init__(self,player):
        self.name = "Player Join Event"
        self.player = player
