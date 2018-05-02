'''
Created on 26 avr. 2018

@author: nroux
'''
from Tkinter import *


class SoloBetatestGUI(Frame):
    '''
    A GUI designed for a single beta-tester:
    One player can play the 5 classes of the game.
    
    This Frame is the master GUI and handles all the other Frame classes below (see GUI draft on github or GDrive)
    '''
    def __init__(self, *args, **kwargs):
        Frame.__init__(self,*args, **kwargs)
        #self.configure(cnf)
        raise NotImplementedError

class WorldMapFrame(Frame):
    '''
    Handles the representation of the revealed board tiles
    '''
    def __init__(self, *args, **kwargs):
        Frame.__init__(self,*args, **kwargs)

class PassiveTribeFrame(Frame):
    '''
    Handles the representation of the passive tribe status and food needs
    '''
    def __init__(self, *args, **kwargs):
        Frame.__init__(self,*args, **kwargs)

class ActivePlayerFrame(Frame):
    '''
    Handles the representation of the active player representation (maybe not useful in solo beta-testing) 
    '''
    def __init__(self, *args, **kwargs):
        Frame.__init__(self,*args, **kwargs)
        
class TurnCounterFrame(Frame):
    '''
    Handles the representation of the current turn count, and the end turn button
    '''
    def __init__(self, *args, **kwargs):
        Frame.__init__(self,*args, **kwargs)
        
class ActorSelectionFrame(Frame):
    '''
    Handles the selection by the user of the Meeple or Group which will perform the action
    '''
    def __init__(self, *args, **kwargs):
        Frame.__init__(self,*args, **kwargs)
        
class ActionSelectionFrame(Frame):
    '''
    Handles the selection by the user of the desired action (costing, or free)
    '''
    def __init__(self, *args, **kwargs):
        Frame.__init__(self,*args, **kwargs)
        
class TargetSelectionFrame(Frame):
    '''
    Handles the selection by the user of the target of selected action.
     Can be a Meeple, a Group, a direction (to move), or None(Hunt) 
    '''
    def __init__(self, *args, **kwargs):
        Frame.__init__(self,*args, **kwargs)
        
class MeepleStatusFrame(Frame):
    '''
    Handles the representation of all the Meeple and their status (remaining AP, Equipment, condition, owner)
    '''
    def __init__(self, *args, **kwargs):
        Frame.__init__(self,*args, **kwargs)

class ConsoleFrame(Frame):
    '''
    Handles the consoles output of the GUI.
    Useful for event, encounters, ...
    '''
    def __init__(self, *args, **kwargs):
        Frame.__init__(self,*args, **kwargs)