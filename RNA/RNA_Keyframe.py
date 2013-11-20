from .RNA_Property import *

class RNA_Keyframe(RNA_Prop):

    def __init__(self, time, value, desc=''):
        assert value.keyable
        super(self.__class__,self).__init__(value, desc)
        self.time = time
    def get(self):
        return self.value
    def get_time(self):
        return self.time

    def set(self, value):
        self.value = value
    def set_time(self, time):
        self.time = time

    def __lt__(self, other):
        return self.time < other.time
    def __gt__(self, other):
        return self.time > other.time
    def __str__(self):
        return '[%s]: %s, Time: %d Value: %s' \
                %(self.__class__.__name__,
                        str(self.info), self.time,str(self.value))

