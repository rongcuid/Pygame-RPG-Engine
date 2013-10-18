'''
Created on Sep 1, 2013

@author: carl
'''
# ----------------------------------

import pygame
from pygame.locals import *
import GameConstants as GC
import Events
from Debug import Debug

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
        return [charactor, sector]

    def GetMoveData(self):
        return [self.characters[0]]

    def SetGame(self, game):
        self.game = game

    def SetData(self, playerDict):
        self.name = playerDict['name']

    def Notify(self, event):
        pass
#---------------------------------


class Charactor:
    count = 0
    def __str__(self):
        return "Charactor ID " + str(self.identity) + \
                " at coordinate " + str(self.coordinate)
    def __init__(self, evManager, sprite = None):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        # This is a tile data
        self.sector = None
        # This is the coordinate
        self.coordinate = (None, None)
        # Set sprite
        self.sprite = sprite
        # Set ID
        # TODO: Will be replaced by RNA
        Charactor.count += 1
        self.identity = Charactor.count

        # Records the previous moving directions
        self.prevDirs = []
        # Records the current moving direction
        self.currDir = None
        
        self.moving = False
        self.moveStartTime = 0

    # --------------------
    def Move(self, direction, facing=None):
        if not facing:
            facing = direction
        if self.sector.CanMove(direction):
           newSector = self.sector.neighbors[direction]
           Debug(newSector)
           self.sector = newSector
           self.UpdateCoordinate()
           ev = Events.CharactorMoveEvent(self)
           self.evManager.Post(ev)

    #------------------------------
    def Place(self, sector, facing=GC.DIRECTION_UP):
        self.sector = sector
        self.UpdateCoordinate()
        ev = Events.CharactorPlaceEvent(self)
        self.evManager.Post(ev)
    #----------------------------
    def GetSprite(self, sprite):
        return self.sprite

    #----------------------------
    def SetSprite(self, sprite):
        '''
        @type sprite: CharactorSprite
        '''
        self.sprite = sprite

    #--------------
    def UpdateCoordinate(self):
        self.coordinate = (self.sector.x, self.sector.y)

    #--------------------------
    def Notify(self, event):
        if isinstance(event, Events.GameStartedEvent):
            gameMap = event.game.map
            #self.Place(gameMap.sectors[gameMap.startSectorIndex])
            # Temporary Test Code
            self.Place(gameMap.sectors[0][0])
            #-------------------
        elif isinstance(event, Events.CharactorMoveRequest):
            self.Move(event.direction)
        elif isinstance(event, Events.LogicTickEvent):
            # TODO: Use Speed instead of that arbitrary time interval
            if not self.moving:
                if self.currDir != None:
                    self.Move(self.currDir)
                    self.moving = True
                    self.moveStartTime = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() > self.moveStartTime + 100:
                    self.moving = False
            # ---------
            self.sprite.Update()
        elif isinstance(event, Events.KeyPressedEvent):
            # TODO: If GUI is on, don't move
            if event.key == K_RIGHT:
                if self.currDir != GC.DIRECTION_RIGHT: # Direction changed
                    if self.currDir != None:
                        self.prevDirs.append(self.currDir) # Store Direction
                    self.currDir = GC.DIRECTION_RIGHT
            elif event.key == K_LEFT:
                if self.currDir != GC.DIRECTION_LEFT: # Direction changed
                    if self.currDir != None:
                        self.prevDirs.append(self.currDir) # Store Direction
                    self.currDir = GC.DIRECTION_LEFT

            elif event.key == K_UP:
                if self.currDir != GC.DIRECTION_UP: # Direction changed
                    if self.currDir != None:
                        self.prevDirs.append(self.currDir) # Store Direction
                    self.currDir = GC.DIRECTION_UP

            elif event.key == K_DOWN:
                if self.currDir != GC.DIRECTION_DOWN: # Direction changed
                    if self.currDir != None:
                        self.prevDirs.append(self.currDir) # Store Direction
                    self.currDir = GC.DIRECTION_DOWN

        elif isinstance(event, Events.KeyReleasedEvent):
            if event.key == K_RIGHT:
                if self.currDir == GC.DIRECTION_RIGHT:
                    if self.prevDirs != []:
                        self.currDir = self.prevDirs.pop()
                    else:
                        self.currDir = None
                # Remove from prevDirs if not currDir
                else:
                    self.prevDirs.remove(GC.DIRECTION_RIGHT)

            elif event.key == K_LEFT:
                if self.currDir == GC.DIRECTION_LEFT:
                    if self.prevDirs != []:
                        self.currDir = self.prevDirs.pop()
                    else:
                        self.currDir = None
                # Remove from prevDirs if not currDir
                else:
                    self.prevDirs.remove(GC.DIRECTION_LEFT)

            elif event.key == K_UP:
                if self.currDir == GC.DIRECTION_UP:
                    if self.prevDirs != []:
                        self.currDir = self.prevDirs.pop()
                    else:
                        self.currDir = None
                # Remove from prevDirs if not currDir
                else:
                    self.prevDirs.remove(GC.DIRECTION_UP)

            elif event.key == K_DOWN:
                if self.currDir == GC.DIRECTION_DOWN:
                    if self.prevDirs != []:
                        self.currDir = self.prevDirs.pop()
                    else:
                        self.currDir = None
                # Remove from prevDirs if not currDir
                else:
                    self.prevDirs.remove(GC.DIRECTION_DOWN)


class CharactorSprite(pygame.sprite.Sprite):
    count = 0
    def __init__(self, charactor, surface):
        pygame.sprite.Sprite.__init__(self)

        charactorSurf = pygame.Surface((GC.TILESIZE,
            GC.TILESIZE))
        charactorSurf = charactorSurf.convert_alpha()
        charactorSurf.fill((0,0,0,0)) # Transparent
        charactorSurf.blit(surface,(0,0))

        self.image = charactorSurf
        self.rect = charactorSurf.get_rect()

        CharactorSprite.count += 1
        self.identity = CharactorSprite.count

        self.charactor = charactor
        # The new position of sprite
        self.moveTo = None

    def Update(self):
        if self.moveTo:
            self.rect.topleft = self.moveTo
            self.moveTo = None

