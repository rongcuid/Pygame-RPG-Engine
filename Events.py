'''
This file contains all types of events in the game
'''

from Debug import Debug

class Event():

    '''
    Superclass of all events
    '''

    def __init__(self):
        self.name = "Generic Event"

    def __str__(self):
        return '<%s %s>' % (self.__class__.__name__, id(self))


class TickEvent(Event):

    def __init__(self):
        self.name = "CPU Tick Event"


class SecondEvent(Event):

    def __init__(self):
        self.name = "Clock One Second Event"


class LogicTickEvent(Event):

    def __init__(self, game):
        self.name = "Logic Tick Event"
        #self.game = game


class QuitEvent(Event):

    def __init__(self):
        self.name = "Quit Event"


class FatalEvent(Event):

    def __init__(self):
        self.name = "Fatal Error Event"


class MapBuiltEvent(Event):

    def __init__(self, map):
        self.name = "Map Built Event"
        self.map = map


class GameStartRequest(Event):

    def __init__(self):
        self.name = "Game Start Request"


class GameStartedEvent(Event):

    def __init__(self, game):
        self.name = "Game Started Event"
        self.game = game


class CharactorMoveRequest(Event):

    def __init__(self, player, charactor, direction):
        self.name = "Charactor Move Request"
        self.player = player
        self.charactor = charactor
        self.direction = direction


class CharactorMoveEvent(Event):

    def __init__(self, charactor):
        self.name = "Charactor Move Event"
        Debug(charactor)
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
        Debug(charactor)
        self.charactor = charactor

class KeyPressedEvent(Event):
    '''
    Key pressed
    '''
    def __init__(self, key):
        self.name = "Key Pressed Event"
        self.key = key

class KeyReleasedEvent(Event):
    '''
    Key released
    '''
    def __init__(self, key):
        self.name = "Key Released Event"
        self.key = key
class WindowResizeRequest(Event):
    '''
    Request to resize window
    '''
    def __init__(self, size):
        self.name = "Window Resize Request Event"
        self.size = size

