'''
Created on Aug 30, 2013

This file includes the RNA_Info class which stores basic information
of RNA structure. The class itself also stores ALL information

@author: carl
'''
from .RNA_Property import *
from .RNA_Structure import *

class RNA_Info():
    '''
    This class stores the basic information of RNA structure.
    Eg. name, description, id
    The class itself also stores all ids
    '''
    # This stores the previous ID assigned
    prevID = 0
    # This stores all names and objects
    nameDict = {}
    # This stores a list of all names
    nameList = []
    
    def __init__(self,desc=""):
        '''
        Renew the ID, initializes an RNA_Info object, and record it
        to nameDict
        @type desc: String
        '''
        # Gives a new, non-repetitive ID
        RNA_Info.prevID += 1
        # Assign the new ID
        self.id = RNA_Info.prevID
                # Record name to nameDict
        RNA_Info.nameDict["self.name"] = self
        # Assign description
        self.description = desc
        # To tell that this RNA_Info is not used
        self.assigned = False
        
    def assign(self, rnaObj):
        '''
        Assign a RNA object to RNA_Info object
        '''
        if not self.assigned and \
                (isinstance(rnaObj,RNA_Prop) or \
                isinstance(rnaObj, RNA_Struct)):
            # Stores the RNA Object contain
            self.contain = rnaObj
            # To tell that this RNA_Info object is used
            self.assigned = True
        else:
            raise Exception("[RNA_Info]This RNA_Info ",self,"cannot assign object ",rnaObj,"!")
        

    def getDesc(self):
        return self.description
    def getID(self):
        return self.id
    
    @classmethod
    def checkNameUnique(cls,name):
        for n in cls.nameList:
            if name == n:
                raise Exception("[RNA_Info]The name ",name,"is not unique!")
    
    @classmethod
    def retrieve(cls,name):
        '''
        Retrieves an RNA_Info object from name
        '''
        for n in cls.nameList:
            if n == name:
                return cls.nameDict[name]
        raise Exception("[RNA_Info]The object with name ",name,"does not exist!")   

