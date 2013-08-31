'''
Created on Aug 31, 2013

@author: carl
'''
import pygame
from pygame.locals import *
from GameConstants import *
import Events
import EventManager

class KeyboardController():
    '''
    Controller for keyboard
    '''


    def __init__(self, evManager, playerName = None):
        '''
        When playerName specified, KeyboardController only controls
        the player specified
        '''
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        
        self.activePlayer = None
        self.playerName = playerName
        self.players = []
    
    def Notify(self,event):
        # TODO: Not finished, still testing
        if isinstance(event,Events.TickEvent):
            # Handles Input
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = Events.QuitEvent
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    ev = Events.QuitEvent
                elif event.type == KEYDOWN and event.key == K_UP:
                    if not self.activePlayer:
                        continue
                    direction = DIRECTION_UP
                    data = self.activePlayer.GetMoveData()
                    ev = Event.CharactorMoveRequest(self.activePlayer, 
                                                    data[0],direction)
                    
# ------------------------------------------
class CPUSpinnerController():
    '''
    Loop forever and post TickEvent
    '''
    def __init__(self,evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        
        self.keepGoing = 1
    def Run(self):
        while self.keepGoing:
            event = Events.TickEvent
            self.evManager.Post(event)
    def Notify(self, event):
        if isinstance(event, Events.QuitEvent):
            self.keepGoing = False
            
# -----------------------------
class SectorSprite(pygame.sprite.Sprite):
    def __init__(self,sector,group=None):
        pygame.sprite.Sprite.__init__(self,group)
        self.image = pygame.Surface((128,128))
        self.image.fill((0,255,128))
        
        self.sector = sector
        
# ----------------------------
class CharactorSprite(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self,group)
        
        charactorSurf = pygame.Surface((64,64))
        charactorSurf = charactorSurf.convert_alpha()
        charactorSurf.fill((0,0,0,0)) # RGBA, transparent
        pygame.draw.circle( charactorSurf (255,0,0), (32,32), 32 )
        self.image = charactorSurf
        self.rect = charactorSurf.get_rect()
        
        self.moveTo = None
    
    def update(self):
        '''
        Move self to self.moveTo
        '''
        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None
            
# --------------------------------------
class PygameView():
    '''
    The View part of the engine
    '''
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        
        pygame.init()
        self.window = pygame.display.set_mode( (424,440) )
        pygame.display.set_caption( 'Test Game with copied code' )
        self.background = pygame.Surface( self.window.get_size())
        self.background.fill((0,0,0))
        
        self.backSprites = pygame.sprite.RenderUpdates()
        self.frontSprites = pygame.sprite.RenderUpdates()
    # -----------------------------------------
    def ShowMap(self,gameMap):
        squareRect = pygame.Rect( (-128,10,128,128) )
        
        i = 0
        for sector in gameMap.sectors:
            if i < 3:
                squareRect = squareRect.move (138,0)
            else:
                i = 0
                squareRect = squareRect.move(-(138*2),138)
                i += 1
                newSprite = SectorSprite(sector, self.backSprites)
                newSprite.rect = squareRect
                newSprite = None
    # ---------------------------------
    def ShowCharactor(self, charactor):
        charactorSprite = CharactorSprite( self.frontSprites )
        
        sector = charactor.sector
        sectorSprite = self.GetSectorSprite( sector )
        charactorSprite.rect.center = sectorSprite.rect.center
    
    # ----------------------------------
    def MoveCharactor(self, charactor):
        charactorSprite = self.GetCharactorSprite( charactor )
        
        sector = charactor.sector
        sectorSprite = self.GetSectorSprite ( sector )
        
        charactorSprite.moveTo = sectorSprite.rect.center
    # -----------------
    def GetCharacterSprite(self, charactor):
        for s in self.frontSprites:
            return s
        return None
    
    # -------------------------------
    def GetSectorSprite(self, sector):
        for s in self.backSprites:
            if hasattr(s, "sector") and s.sector == sector:
                return s
    
    # ---------------------------
    def Notify(self,event):
        if isinstance( event, Events.TickEvent ):
            # Draw everything
            self.backSprites.clear( self.window, self.background )
            self.frontSprites.clear( self.window, self.background )
            
            self.backSprites.update()
            self.frontSprites.update()
            
            dirtyRects1 = self.backSprites.draw(self.window)
            dirtyRects2 = self.frontSprites(self.window)
            
            dirtyRects = dirtyRects1 + dirtyRects2
            pygame.display.update( dirtyRects )
        elif isinstance(event, Events.MapBuiltEvent):
            gameMap = event.map
            self.ShowMap(gameMap)
        elif isinstance(event, CharactorPlaceEvent):
            self.ShowCharactor(event.charactor)
        
        elif isinstance(event,CharactorMoveEvent):
            self.MoveCharactor(event.charactor)

#--------------------------------------------------
class Game:
    '''
    Main game class
    '''
    
    # Game states
    STATE_PREPARING = 0
    STATE_RUNNING = 1
    SELF_PAUSED = 2
    
    #-----------------
    def __init__(self,evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        
        self.state = Game.STATE_PREPARING
        
        self.players = [ Player(evManager) ]
        self.map = Map(evManager)
        
    #-----------------------------
    def Start(self):
        self.map.Build()
        self.state = Game.STATE_RUNNING
        ev = Events.GameStartedEvent(self)
        self.evManager.Post(ev)
    
    #-----------------
    def Notify(self, event):
        if isinstance(event, Events.TickEvent):
            if self.state == Game.STATE_PREPARING:
                self.Start()

# ----------------------------------
class Player:
    def __init__(self, evManager):
        self.evManager = evManager
        
        self.charactors = [Charactor(evManager)]
        
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
            ev = CharactorMoveEvent( self )
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
        elif isinstance(event, CharactorMoveRequet):
            self.Move(event.direction)
            
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
        
        self.sectors = range(9)
        self.startSectorIndex = 0
    
    #-----------------------------------
    def Build(self):
        for i in range(9):
            self.sectors[i] = Sector( self.evManager )
            
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
        
        self.neighbors = range(4)
        
        self.neighbors[DIRECTION_UP] = None
        self.neighbors[DIRECTION_DOWN] = None
        self.neighbors[DIRECTION_LEFT] = None
        self.neighbors[DIRECTION_RIGHT] = None
        
    def MovePossible(self,direction):
        if self.neighbors[direction]:
            return 1
#--------------------
def main():
    evManager = EventManager.EventManager
    
    keybd = KeyboardController(evManager)
    spinner = CPUSpinnerController(evManager)
    pygameView = PygameView(evManager)
    game = Game(evManager)
    
    spinner.Run()
    
if __name__ == "__main__":
    main()
