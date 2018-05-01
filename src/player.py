'''
Created on 26 avr. 2018

@author: nroux
'''
CRAFTSMAN_MAX_MEEPLE_COUNT = 4
SHAMAN_MAX_MEEPLE_COUNT = 4
GATHERER_MAX_MEEPLE_COUNT = 4
ELDER_MAX_MEEPLE_COUNT = 4
TRACKER_MAX_MEEPLE_COUNT = 4
from meeple import Craftsman, Elder, Gatherer, Shaman, Tracker



class Player(object):
    '''
    Each instance of this class represents one player of a physical game. Therefore, each Player instance handles its own meeple collection.
    '''


    def __init__(self, game, player_id, player_name, meeple_type):
        '''
        Constructor
        '''
        self.id = player_id
        self.name = player_name
        self.meeple_type = meeple_type
        self.is_eliminated = False
        self.meeple_array = []
        if meeple_type == "Craftsman":
            for dummy in range(CRAFTSMAN_MAX_MEEPLE_COUNT):
                self.meeple_array.append(Craftsman(owner=self))
        elif meeple_type == "Elder":
            for dummy in range(ELDER_MAX_MEEPLE_COUNT):
                self.meeple_array.append(Elder(owner=self))
        elif meeple_type == "Gatherer":
            for dummy in range(GATHERER_MAX_MEEPLE_COUNT):
                self.meeple_array.append(Gatherer(owner=self))
        elif meeple_type == "Shaman":
            for dummy in range(SHAMAN_MAX_MEEPLE_COUNT):
                self.meeple_array.append(Shaman(owner=self))
        elif meeple_type == "Tracker":
            for dummy in range(TRACKER_MAX_MEEPLE_COUNT):
                self.meeple_array.append(Tracker(owner=self))
        else: raise NameError("Wrong player Class. Please chose on of the following : Craftsman, Shaman, Elder, Gatherer, Tracker.")        
    
    def take_turn(self):
        '''
        Player is invited by the GUI to take actions. These are handled by the meeple superclass and subclasses and the GUI class.
        TODO : Check if a meeple start its turn with a non-healed major bleeding -> ded
        '''
        raise NotImplementedError
            
        