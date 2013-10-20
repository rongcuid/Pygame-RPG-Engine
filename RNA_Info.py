'''
Created on Aug 30, 2013

This file includes the InfoRNA class which stores basic information
of RNA structure. The class itself also stores ALL information

@author: carl
'''

class InfoRNA():
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
        Renew the ID, initializes an InfoRNA object, and record it
        to nameDict
        @type desc: String
        '''
        # Gives a new, non-repetitive ID
        InfoRNA.prevID += 1
        # Assign the new ID
        self.id = InfoRNA.prevID
                # Record name to nameDict
        InfoRNA.nameDict["self.name"] = self
        # Assign description
        self.description = desc
        # To tell that this InfoRNA is not used
        self.assigned = False
        
    def assign(self, rnaObj):
        '''
        Assign a RNA object to InfoRNA object
        '''
        if not self.assigned and type(rnaObj) == PropRNA: #or type(rnaObj) == StructRNA:
            # Stores the RNA Object contain
            self.contain = rnaObj
            # To tell that this InfoRNA object is used
            self.assigned = True
        else:
            raise Exception("[InfoRNA]This InfoRNA ",self,"cannot assign object ",rnaObj,"!")
        

    def getDesc(self):
        return self.description
    def getID(self):
        return self.id
    
    @classmethod
    def checkNameUnique(cls,name):
        for n in cls.nameList:
            if name == n:
                raise Exception("[InfoRNA]The name ",name,"is not unique!")
    
    @classmethod
    def retrieve(cls,name):
        '''
        Retrieves an InfoRNA object from name
        '''
        for n in cls.nameList:
            if n == name:
                return cls.nameDict[name]
        raise Exception("[InfoRNA]The object with name ",name,"does not exist!")   

from PropertyRNA import PropRNA
