'''
Created on Sep 1, 2013

@author: carl
'''
# ----------------------------------

import pygame
from pygame.locals import *

from Imports.common import *

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
        self.facing = None
        
        self.moving = False
        self.moveStartTime = 0

    # --------------------
    def Move(self, direction, facing=None):
        if not facing:
            facing = direction
        self.facing = facing
        if self.sector.CanMove(direction):
           newSector = self.sector.neighbors[direction]
           Debug("Charactor: Move(): ", newSector)
           self.sector = newSector
           self.UpdateCoordinate()
           ev = Events.CharactorMoveEvent(self)
           self.evManager.Post(ev)

    #------------------------------
    def Place(self, sector, facing=GC.DIRECTION_UP):
        self.sector = sector
        self.facing = facing
        self.UpdateCoordinate()
        ev = Events.CharactorPlaceEvent(self)
        self.evManager.Post(ev)
    #----------------------------
    def GetSprite(self, sprite):
        return self.sprite

    #----------------------------
    def SetSprite(self, sprite):
        '''
        @type sprite: CharactorPGSprite
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
            # --------------Moving-----------------
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
            # --------------End Moving-----------------
            # --------------Basic Operation-----------
            elif event.key == K_z:
                ev = Events.SectorCheckRequest(self, self.sector, 
                        self.facing)
                self.evManager.Post(ev)
            # --------------End Basic Operation--------

        elif isinstance(event, Events.KeyReleasedEvent):
            # --------------Moving-----------------
            if event.key == K_RIGHT:
                if self.currDir == GC.DIRECTION_RIGHT:
                    if self.prevDirs != []:
                        self.currDir = self.prevDirs.pop()
                    else:
                        self.currDir = None
                # Remove from prevDirs if not currDir
                else:
                    if GC.DIRECTION_RIGHT in self.prevDirs:
                        self.prevDirs.remove(GC.DIRECTION_RIGHT)

            elif event.key == K_LEFT:
                if self.currDir == GC.DIRECTION_LEFT:
                    if self.prevDirs != []:
                        self.currDir = self.prevDirs.pop()
                    else:
                        self.currDir = None
                # Remove from prevDirs if not currDir
                else:
                    if GC.DIRECTION_LEFT in self.prevDirs:
                        self.prevDirs.remove(GC.DIRECTION_LEFT)

            elif event.key == K_UP:
                if self.currDir == GC.DIRECTION_UP:
                    if self.prevDirs != []:
                        self.currDir = self.prevDirs.pop()
                    else:
                        self.currDir = None
                # Remove from prevDirs if not currDir
                else:
                    if GC.DIRECTION_UP in self.prevDirs:
                        self.prevDirs.remove(GC.DIRECTION_UP)

            elif event.key == K_DOWN:
                if self.currDir == GC.DIRECTION_DOWN:
                    if self.prevDirs != []:
                        self.currDir = self.prevDirs.pop()
                    else:
                        self.currDir = None
                # Remove from prevDirs if not currDir
                else:
                    if GC.DIRECTION_DOWN in self.prevDirs:
                        self.prevDirs.remove(GC.DIRECTION_DOWN)
            # --------------End Moving-----------------
        elif isinstance(event, Events.SectorCheckRequest):
            # Test Code
            Debug("Charactor: Notify(): ", self, self.sector)
            # ---------


class CharactorSprite():
    count = 0
    def __init__(self, charactor, surface):
        self.image = None
        self.rect = None

        self.count += 1
        self.identity = self.count
        
        self.charactor = charactor

        self.moveTo = None

    def Update(self):
        self.moveTo = None

class CharactorPGSprite(CharactorSprite):
    def __init__(self, charactor, surface):
        super(CharactorPGSprite, self).__init__(charactor,
                surface)
        pygame.sprite.Sprite.__init__(self)

        charactorSurf = pygame.Surface((GC.TILESIZE,
            GC.TILESIZE))
        charactorSurf = charactorSurf.convert_alpha()
        charactorSurf.fill((0,0,0,0)) # Transparent
        charactorSurf.blit(surface,(0,0))

        self.image = charactorSurf
        self.rect = charactorSurf.get_rect()

        #self.count += 1
        #self.identity = CharactorPGSprite.count

        #self.charactor = charactor
        # The new position of sprite
        #self.moveTo = None

    def Update(self):
        if self.moveTo:
            self.rect.topleft = self.moveTo
        super(self.__class__, self).Update()

