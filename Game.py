'''
This file is the Model part of the game.
Contains class Game
'''

import sys
# Temporary Test
import pygame
from pygame.locals import *
# ------

from Imports.common import *

import EventManager
import Controllers
import Views
import Map
import Charactor

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
        self.evManager.RegisterListener(self)

        self.state = Game.STATE_PREPARING

        self.map = Map.Map(GC.TEST_LEVEL_MAP, evManager)
        # Test Code    
        self.charactors = [Charactor.Charactor(evManager)]
        img = pygame.image.load("data/Player-test.png")
        sprite = Charactor.CharactorPGSprite(self.charactors[0],img)
        self.charactors[0].SetSprite(sprite)
        self.Start()
        # ----------
    #----------------

    def Start(self):
        self.map.Build()
        self.state = Game.STATE_RUNNING
        ev = Events.GameStartedEvent(self)
        self.evManager.Post(ev)
    #-----------------
    def Notify(self, event):
        # Temporary test code
        if isinstance(event, Events.KeyPressedEvent):
            if event.key == K_RETURN:
                ev = Events.GameStartRequest()
                self.evManager.Post(ev)
                
        # -----------------
        if isinstance(event, Events.GameStartRequest):
            if self.state == Game.STATE_PREPARING:
                self.Start()

#---------------------------------------


def main():
    evManager = EventManager.EventManager()
    # Initialize important controllers/listeners
    keybd = Controllers.KeyboardController(evManager)
    spinner = Controllers.CPUSpinnerController(evManager)
    pygameView = Views.PygameView(evManager)
    # --------------------------
    
    game = Game(evManager)
    # Temp Test Code
    #pygameView.SetTrack(game.charactors[0])
    # -------------
    spinner.Run()


if __name__ == "__main__":
    main()
