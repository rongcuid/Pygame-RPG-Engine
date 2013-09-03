'''
Created on Sep 1, 2013

@author: carl
'''

import pygame
from pygame.locals import *

from GameConstants import *

# -----------------------------
class SectorSprite(pygame.sprite.Sprite):
    def __init__(self,sector,group = None):
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
        pygame.draw.circle( charactorSurf,(255,0,0), (32,32), 32 )
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
            