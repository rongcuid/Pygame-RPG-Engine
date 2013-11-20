'''
Created on Aug 30, 2013

@author: carl
'''

from .RNA_Info import *
from .RNA_Property import *

class RNA_Struct():
    '''
    An RNA object that stores multiple values
    '''


    def __init__(self,desc=""):
        '''
        Initiate one Structure RNA object, and one RNA_Info object
        '''
        # Create info object
        self.info = RNA_Info(desc)
        # Register this object to info object
        self.info.assign(self)
        # Create a list of properties registered
        self.registeredList = []
        
    def register(self,prop):
        '''
        Register a RNA_Prop object
        '''
        if prop in self.registeredList:
            raise Exception(self.__class__.__name__,
                    "Property ",p," has already registered to ",
                    self,"!")
        self.registeredList.append(prop)
