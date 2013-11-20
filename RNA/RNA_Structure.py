'''
Created on Aug 30, 2013

@author: carl
'''

from InfoRNA import InfoRNA
from PropertyRNA import PropRNA

class StructRNA():
    '''
    An RNA object that stores multiple values
    '''


    def __init__(self,desc=""):
        '''
        Initiate one Structure RNA object, and one InfoRNA object
        '''
        # Create info object
        self.info = InfoRNA(desc)
        # Register this object to info object
        self.info.assign(self)
        # Create a list of properties registered
        self.registeredList = []
        
    def register(self,prop):
        '''
        Register a PropRNA object
        '''
        for p in self.registeredList:
            if prop == p:
                raise Exception("[StructRNA]Property ",p," has already registered to ",self,"!")
        self.registeredList += prop
