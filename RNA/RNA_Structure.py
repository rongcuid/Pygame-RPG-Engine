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
        # Create a dict of properties registered
        self.registeredDict = {}
        
    def register(self,name,prop):
        '''
        Register a RNA_Prop object
        '''
        if prop in self.registeredDict.values():
            raise Exception(self.__class__.__name__,
                    "Property ",prop," has already registered to ",
                    self,"!")
        self.registeredDict[name] = prop

    def get(self, name):
        return self.registeredDict.get(name)
    
    def get_all(self):
        return self.registeredDict
