import pygame
from pygame.locals import *

from Debug import Debug

import GameConstants
import EventManager
import Events
import Controllers

#---------------------------------
class PygameView:
    '''
    Pygame View of the game, handles the display
    '''
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        pygame.init()
        self.window = pygame.display.set_mode( (800,600) )
        #self.window.fill((255,255,255))
        pygame.display.set_caption( 'Test Game' )
        self.background = pygame.Surface( self.window.get_size() )
        self.background.fill( (0,255,0) )

        pygame.display.flip()

    #-------------------------------
    def Notify(self,event):
        if isinstance( event, Events.TickEvent ):
            self.window.blit(self.background,(0,0))
            pygame.display.update()

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
    
    #pygame.init()
    #DISPLAYSURF = pygame.display.set_mode((640,400))
    #pygame.display.set_caption('Hello World!')
    #while True:
    #    pygame.display.update()

    pygameView = PygameView( evManager )
    keybd = Controllers.KeyboardController( evManager )
    spinner = Controllers.CPUSpinnerController( evManager )
    #game = Game( evManager )
    spinner.Run()


if __name__ == "__main__":
    main()
