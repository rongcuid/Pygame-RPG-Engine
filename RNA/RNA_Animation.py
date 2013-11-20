from .RNA_Info import *
from .RNA_Property import *
import bisect

class RNA_Animation(RNA_Struct):
    def __init__(self, desc=""):
        super(self.__class__,self).__init__(self, desc)

    def register(self, keyframe):
        if keyframe in self.registeredList:
            raise Exception(self.__class__.__name__,
                    "Keyframe ",p," has already registered to ",
                    self,"!")
        # Insert in order
        index = bisect.bisect_left(self.registeredList, 
                keyframe)
        self.registeredList.insert(index, keyframe)

    def get(self, time):
        # TODO: get value by time
        pass
