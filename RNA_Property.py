'''
Created on Aug 30, 2013

@author: carl
'''

from InfoRNA import InfoRNA

class PropRNA():
    '''
    This class stores a value(property).
    '''
    
    
    def __init__(self,value,desc=""):
        '''
        Creates an InfoRNA object and assign this object to the InfoRNA object,
        then store the value
        '''
        # Create an InfoRNA object
        self.info = InfoRNA(desc)
        # Register this PropRNA to the InfoRNA object just created
        self.info.assign(self)
        # Set value
        self.value = value
    
    def get(self):
        return self.value
    def set(self,value):
        self.value = value
