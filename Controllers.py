'''
This file is the Controller part of the game.
Contains all controllers needed for the game.
'''
import pygame
from pygame.locals import *

from Debug import Debug

import GameConstants
import EventManager
import Events


class KeyboardController():

    '''
    This gets keyboard events and checks key pressed
    '''

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
    #-----------------------

    def Notify(self, event):
        if isinstance(event, Events.TickEvent):
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = Events.QuitEvent()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        ev = Events.QuitEvent()
                    else:
                        ev = Events.KeyPressedEvent(event.key)
                        #ev = Events.GameStartRequest()
                if ev:
                        self.evManager.Post(ev)
# ---------------------------------


class CPUSpinnerController():

    '''
    Send a TickEvent every loop. This determines if the game is running.
    '''

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.keepGoing = True
    #----------------------------

    def Run(self):
        # Record the initialization time
        self.initTime = pygame.time.get_ticks()

        # Time when previous TickEvent was sent
        prevTick = self.initTime
        # Post the first second event
        self.evManager.Post(Events.SecondEvent())
        while self.keepGoing:
            event = Events.TickEvent()
            self.evManager.Post(event)
            # Post a LogicTickEvent every logic cycle
            if self.IntervalPassed(prevTick,
                                   1000 / GameConstants.LOGICRATE):
                self.evManager.Post(Events.LogicTickEvent())
            # Post a SecondEvent every second
            if self.OneSecPassed(prevTick):
                self.evManager.Post(Events.SecondEvent())
            prevTick = pygame.time.get_ticks()
            # pygame.time.Clock().tick(100)

    #----------------------------
    def OneSecPassed(self, prevTick):
        return self.IntervalPassed(prevTick, 1000)
    #----------------------------

    def IntervalPassed(self, prevTick, interval):
        ''' Returns true when interval milliseconds passed '''
        return pygame.time.get_ticks() % interval < prevTick % interval
    #---------------------------

    def Notify(self, event):
        if isinstance(event, Events.QuitEvent):
            self.keepGoing = False
