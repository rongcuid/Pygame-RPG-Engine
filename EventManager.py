'''
Created on Aug 31, 2013

@author: carl
'''

from GameConstants import *
import Events

def Debug(msg):
    print(msg)
    

class EventManager():
    '''
    This class manages all events in the game
    It connects the model-view-control part of the game
    '''
    def __init__(self):
        import weakref
        self.listeners = weakref.WeakKeyDictionary()
        self.eventQueue = []
        self.listenersToAdd = []
        self.listenersToRemove = []
        
    # ------------------
    def RegisterListener(self,listener):
        self.listenersToAdd.append(listener)
    
    #-------------------
    def UnregisterListener(self,listener):
        self.listenersToRemove.append(listener)
    
    # -------------------
    def UpdateListeners(self):
        '''
        Actually updates the list of listeners
        '''
        for l in self.listenersToAdd:
            self.listeners[l] = 1
        for l in self.listenersToRemove:
            if l in self.listeners:
                del self.listeners[l]
        self.listenersToAdd = []
        self.listenersToRemove = []
    
    #------------------
    def Post(self,event):
        '''
        Add an event to queue
        '''
        self.eventQueue.append(event)
        if isinstance(event, Events.TickEvent):
            self.UpdateListeners()
            self.ConsumeEventQueue()
        else:
            Debug("    Message: "+event.name)
    
    # ------
    def ConsumeEventQueue(self):
        i = 0
        while i < len(self.eventQueue):
            event = self.eventQueue[i]
            for listener in self.listeners:
                old = len(self.eventQueue)
                listener.Notify(event)
            i += 1
            if self.listenersToAdd:
                self.UpdateListeners()
        self.eventQueue = []

        