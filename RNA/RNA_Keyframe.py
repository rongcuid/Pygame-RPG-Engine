from .RNA_Prop import *

class RNA_Keyframe(RNA_Prop):

    def __init__(self, time, value, desc=''):
        self.frame = [time, super(self.__class__, self)(value,
            desc)] # List containing time and RNA_Prop
    
    def get(self):
        return self.frame[1]
    def get_time(self):
        return self.frame[0]

    def set(self, value):
        self.frame[1] = value
    def set_time(self, time):
        self.frame[0] = time

    def __lt__(self, other):
        return self.frame[0] < other.frame[0]
    def __gt__(self, other):
        return self.frame[0] > other.frame[0]
