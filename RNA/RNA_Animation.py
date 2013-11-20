from .RNA_Info import *
from .RNA_Property import *
from .RNA_Structure import *
import bisect

class RNA_Animation(RNA_Struct):
    def __init__(self, desc=""):
        super(self.__class__,self).__init__(desc)
        # Store the value type to be stored
        self.valueType = None

        # Current time on timeline
        self.time = 0

        # Start frame
        self.start = 0
        # End frame
        self.end = 0

    def set(self, keyframe):
        if not self.valueType:
            self.valueType = keyframe.value.__class__
        elif keyframe.value.__class__ != self.valueType:
            raise Exception(
                    "[%s]: Keyframe %s has different type %s to the accepted type %s in animation" \
                            %(self.__class__.__name__, keyframe, 
                                keyframe.__class__.__name__,
                                self.valueType.__name__))
        if keyframe in self.registeredDict.values():
            raise Exception(self.__class__.__name__,
                    "Keyframe ",keyframe," has already registered to ",
                    self,"!")
        self.registeredDict[keyframe.time] = keyframe

    def get_prev(self, time):
        ''' 
        Get the previous keyframe before time
        '''
        frames = sorted(self.registeredDict.keys())
        if time < frames[0]:
            return None
        index = bisect.bisect(frames, time) - 1
        return self.registeredDict.get(frames[index])

    def get_next(self, time):
        '''
        Get the next keyframe after time
        '''
        frames = sorted(self.registeredDict.keys())
        index = bisect.bisect(frames, time)
        if index >= len(frames):
            return None
        return self.registeredDict.get(frames[index])

    def get(self, time=None):
        '''
        Get the value using time.
        '''
        if time == None:
            time = self.time
        prev_frame = self.get_prev(time)
        next_frame = self.get_next(time)
        
        if prev_frame == None and next_frame == None:
            return None
        elif prev_frame == None:
            return next_frame.value.value
        elif next_frame == None:
            return prev_frame.value.value

        if self.valueType == RNA_Prop_Int:
            '''
            Let prev time be t1, next time be t2, 
            corresponding value
            be v1 and v2, and the current time is t and value is v,
            then:
            v = v1 + (v2-v1) * (t - t1) / (t2 - t1)
            This is a simple linear approach
            '''
            return self.linear_approx(prev_frame, next_frame,
                    time, True)
        elif self.valueType == RNA_Prop_Float:
            return self.linear_approx(prev_frame, next_frame,
                    time, False)
        elif self.valueType == RNA_Prop_Bool:
            return prev_frame.value.value

    def linear_approx(self, prev_frame, next_frame, time, integer=False):
        value = prev_frame.value.value + \
                (next_frame.value.value -\
                prev_frame.value.value) * \
                ((time - prev_frame.time) / \
                (next_frame.time - prev_frame.time))
        if integer:
            value = int(value)
        return value

    def step(self, step = 1):
        time = self.time + step
        if time >= self.start and time <= self.end:
            self.time = time
    def set_time(self, time):
        if time < self.start:
            self.time = self.start
        elif time > self.end:
            self.time = self.end
        else:
            self.time = time


    def set_start(self, start):
        self.start = start
    def set_end(self, end):
        self.end = end
