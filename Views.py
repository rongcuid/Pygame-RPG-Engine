'''
This file is the View part of the game.
Contains class PygameView
'''
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


