import pygame
from pygame.locals import *

from Debug import Debug

import GameConstants
import EventManager
import Events


#-----------------------------
class KeyboardController():
    '''
    This gets keyboard events and checks key pressed
    '''
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )
    #-----------------------
    def Notify(self,event):
        if isinstance( event, Events.TickEvent ):
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = Events.QuitEvent()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        ev = Events.QuitEvent()
                if ev:
                        self.evManager.Post( ev )
# ---------------------------------
class CPUSpinnerController():
    '''
    Send a TickEvent every loop. This determines if the game is running.
    '''
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        self.keepGoing = True
    #----------------------------
    def Run(self):
        while self.keepGoing:
            event = Events.TickEvent()
            self.evManager.Post(event)
    #---------------------------
    def Notify(self,event):
        if isinstance (event, Events.QuitEvent):
            self.keepGoing = False

#---------------------------------
class PygameView:
    '''
    Pygame View of the game, handles the display
    '''
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        pygame.init()
        self.window = pygame.display.set_mode( (424,440) )
        pygame.display.set_caption( 'Test Game' )
        self.background = pygame.Surface( self.window.get_size() )
        self.background.fill( (0,255,0) )
        font = pygame.font.Font(None, 30)
        text = "Test Text"
        textImg = font.render( text, 1, (255,0,0))
        self.background.blit( self.background, (0,0) )
        pygame.display.flip()

        self.backSprites = pygame.sprite.RenderUpdates()
        self.frontSprites = pygame.sprite.RenderUpdates()
    #-------------------------------
    def Notify(self,event):
        if isinstance( event, Events.TickEvent ):
            self.backSprites.clear( self.window, self.background )
            self.frontSprites.clear( self.window, self.background )

            self.backSprites.update()
            self.frontSprites.update()

            dirtyRect1 = self.backSprites.draw( self.window )
            dirtyRect2 = self.frontSprites.draw( self.window )

            dirtyRects = dirtyRect1 + dirtyRect2
            pygame.display.update( dirtyRects )

#--------------------------------------
class Game:
    STATE_PREPARING = 'Preparing'
    STATE_RUNNING = 'Running'
    STATE_PAUSED = 'Paused'

    #-----------------
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        self.state = Game.STATE_PREPARING

#---------------------------------------
def main():
    evManager = EventManager.EventManager()
    
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((640,400))
    pygame.display.set_caption('Hello World!')
    #while True:
    #    pygame.display.update()

    spinner = CPUSpinnerController( evManager )
    keybd = KeyboardController( evManager )
    #pygameView = PygameView( evManager )
    #game = Game( evManager )
    spinner.Run()


if __name__ == "__main__":
    main()
