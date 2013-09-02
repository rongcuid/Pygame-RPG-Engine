'''
This file is the Model part of the game.
Contains class Game
'''
import pygame
from pygame.locals import *

from Debug import Debug

import GameConstants
import EventManager
import Events
import Controllers
import Views

#--------------------------------------
class Game:
    '''
    Main game class
    '''
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

    keybd = Controllers.KeyboardController( evManager )
    spinner = Controllers.CPUSpinnerController( evManager )
    pygameView = Views.PygameView( evManager )

    game = Game( evManager )
    spinner.Run()


if __name__ == "__main__":
    main()
