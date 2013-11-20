'''
Created on Aug 30, 2013

@author: carl
'''

from .RNA_Info import *

class RNA_Prop():
    '''
    This class stores a value(property).
    '''
    
    
    def __init__(self,value,desc=""):
        '''
        Creates an RNA_Info object and assign this object to the InfoRNA object,
        then store the value
        '''

        # Create an RNA_Info object
        self.info = RNA_Info(desc)
        # Register this RNA_Prop to the RNA_Info object just created
        self.info.assign(self)
        # Set value
        self.value = value
        # If the current type is keyable
        self.keyable = False
        # Set animation
        self.animation = None
    
    def get(self, time=None):
        if self.animation != None:
            return self.animation.get(time)
        return self.value
    def set(self,value):
        self.value = value
    def set_animation(self, animation):
        self.animation = animation
    def del_animation(self):
        if self.animation != None:
            self.value = self.animation.get()
            del self.animation

    def set_time(self, time):
        if self.animation != None:
            self.animation.set_time(time)
    def step(self, step=1):
        if self.animation != None:
            self.animation.step(step)

    def __lt__(self, other):
        return self.value < other.value
    def __gt__(self, other):
        return self.value > other.value
    def __str__(self):
        return '[%s]: %s, Value: %s' \
                %(self.__class__.__name__,
                        str(self.info),str(self.value))

class RNA_Prop_Bool(RNA_Prop):
    def __init__(self, value, desc=''):
        assert isinstance(value, bool)
        super(self.__class__,self).__init__(value, desc)
        self.keyable = True

class RNA_Prop_Int(RNA_Prop):
    def __init__(self, value, desc=''):
        assert isinstance(value, int) or isinstance(value,float)
        super(self.__class__,self).__init__(int(value), desc)
        self.keyable = True

class RNA_Prop_Float(RNA_Prop):
    def __init__(self, value, desc=''):
        assert isinstance(value, float) or isinstance(value, int)
        super(self.__class__,self).__init__(float(value), desc)
        self.keyable = True

class RNA_Prop_String(RNA_Prop):
    def __init__(self, value, desc=''):
        assert isinstance(value, str)
        super(self.__class__,self).__init__(value, desc)
        self.keyable = False

