'''
Created on 26 avr. 2018

@author: nroux
'''
from random import randint

HEALTHY = 0
HANDICAP = 1
MINOR_BLEEDING = 10
MAJOR_BLEEDING = 100
FEVER = 1000
DEATH = 10000


class Meeple(object):
    '''
    Abstract class handling all the basic actions that can be performed by all different Meeple classes.
    Classes that have bonuses to certain actions will override parent method
    '''
    # Static attriute
    max_action_point = 6
    def __init__(self, player):
        '''
        Constructor
        '''
        self.player = player
        self.condition = HEALTHY
        # Starting tile
        self.position = player.game.tiles[0]
        self.equipment = []
        self.action_point_count = Meeple.max_action_point
        
        
    def rollD6(self):
        return randint(1,6)
    def roll2D6(self):
        return self.rollD6()+self.rollD6()
    def refill_action_points(self):
        self.action_point_count = Meeple.max_action_point
    def is_healthy(self):
        return self.condition == HEALTHY
    def is_handicapped(self):
        return self.condition%(10*HANDICAP)>= HANDICAP
    def is_minor_bleeding(self):
        return self.condition%(10*MINOR_BLEEDING)>= MINOR_BLEEDING
    def is_major_bleeding(self):
        return self.condition%(10*MAJOR_BLEEDING)>= MAJOR_BLEEDING
    def is_bleeding(self):
        return self.is_minor_bleeding() or self.is_major_bleeding()
    def is_feverish(self):
        return self.condition%(10*FEVER)== FEVER
    def is_dead(self):
        return self.condition >= DEATH
    def action_move(self, direction):
        raise NotImplementedError
    def action_explore(self):
        raise NotImplementedError
    def action_hunt(self):
        raise NotImplementedError
    def action_gather(self):
        raise NotImplementedError
    def action_craft(self, crafted_item_id):
        raise NotImplementedError
    def action_create_home(self):
        raise NotImplementedError
    def action_fire(self):
        raise NotImplementedError
    def join_group(self, Group):
        raise NotImplementedError
    def leave_group(self):
        raise NotImplementedError
    
class Group(object):
    '''
    classdocs
    '''

    
    def __init__(self, params):
        '''
        Constructor
        '''
        

class Craftsman(Meeple):
    '''
     Rules :
         Skilled hands : +1 to the roll when crafting an object
         Ingenious : 50% chance to recover materials after a failed creation
         Adaptable genius : a craftsman can create basic objects outside of the rock shelter
         
         
         @Hadrien : si un jour tu passes par là, et que tu modifies la classe ARTISAN, écris ici <3
    '''

    carrying_capacity = 2 
    
    def __init__(self, params):
        '''
        Constructor
        '''
    def action_craft(self, crafted_item_id):
        '''
        Overrides parent methods. See above classdocs
        '''
        Meeple.action_craft(self, crafted_item_id)
        raise NotImplementedError


class Elder(Meeple):
    '''
    Rules : 
        . Fire mastering : a group creating fire always suceed
        . Medical science [1 AP] : cures a minor wound of a character in the Group (remove handicap)
        . Wise advice : if an Elder is in a group, any member of the group can perform an action with a pre-requisite if the Elder fulfills this pre-requisite
        . Acuity : the group can re-roll the encounter roll (keep NEW ROLL, can't keep old one)
        . Hunting techniques : what ?
    '''
    carrying_capacity = 1
    
    def __init__(self, params):
        '''
        Constructor
        '''
    
    def action_fire(self):
        '''
        Overrides parent methods. See above classdocs
        '''
        raise NotImplementedError
    def action_medical_science(self, target_meeple):
        '''
        . Medical science [1 AP] : cures a minor wound of a character in the Group (remove handicap)
        '''
        Shaman.action_medical_science(self, target_meeple)    
    def action_hunt(self):
        '''
        See Hunting techniques in rules
        '''
        Meeple.action_hunt(self)
        raise NotImplementedError
    
class Shaman(Meeple):
    '''
    Rules : 
    . Medical science [1 AP] : cures a minor wound of a character in the Group (remove handicap)
    . Heal [1AP+plant] : remove bleeding or fever
    . Cure [1AP + cataplasm plant] : remove Major bleeding
    . Painting science : can craft pigment and ointment
    . Plant science : can gather plants with the gather action
    . Sacred art : apparently, no one else can draw a horse with his fingers
    '''
    carrying_capacity = 1
    
    def __init__(self, params):
        '''
        Constructor
        '''
    
    def action_medical_science(self, target_meeple):
        '''
        . Medical science [1 AP] : cures a minor wound of a character in the Group (remove handicap)
        '''
        raise NotImplementedError
    
    def action_heal(self, target_meeple):
        '''
        . Heal [1AP+plant] : remove bleeding or fever
        '''
        raise NotImplementedError
    
    def action_cure(self, target_meeple):
        '''
        . Cure [1AP + cataplasm plant] : remove Major bleeding
        '''
    def action_gather(self):
        '''
        . Plant science : can gather plants with the gather action
        '''
        Meeple.action_gather(self)
    
    def action_craft(self, crafted_item_id):
        '''
        . Painting science : can craft pigment and ointment
        '''
        Meeple.action_craft(self, crafted_item_id)
        raise NotImplementedError
    def action_parietal_art(self):
        '''
        . Sacred art : can create a work of art in a cave (win condition)
        '''
        raise NotImplementedError
        
class Gatherer(Meeple):
    '''
    Rules : 
    . Plant science : can gather plants with the gather action
    . Explorer : +1 to the exploration roll (!!!!)  to discover a POI
    . Heal [1AP+plant] : remove bleeding or fever
    . Skilled gatherer : can search for fruits in forest for free AP 
    '''
    carrying_capacity = 2

    
    def __init__(self, params):
        '''
        Constructor
        '''
    def action_gather(self):
        '''
        . Plant science : can gather plants with the gather action
        '''
        Shaman.action_gather(self)
    
    def action_explore(self):
        '''
        . Explorer : +1 to the exploration roll (!!!!)  to discover a POI
        '''
        Meeple.action_explore(self)
        raise NotImplementedError
    def action_heal(self, target_meeple):
        '''
        . Heal [1AP+plant] : remove bleeding or fever
        '''
        Shaman.action_heal(self, target_meeple)
        
class Tracker(object):
    
    '''
    Rules : 
    . Expert tracker : while hunting, roll a dice to determine if predators are encountered. If not, the Tracker can chose the encountered prey
    . Skilled hunter : +1 to the combat score while attacking a prey
    . Gifted explorer : Can re-roll after a failed POI exploration
    '''
    
    carrying_capacity = 2

    def __init__(self, params):
        '''
        Constructor
        '''
    def action_hunt(self):
        '''
        . Expert tracker : while hunting, roll a dice to determine if predators are encountered. If not, the Tracker can chose the encountered prey
        . Skilled hunter : +1 to the combat score while attacking a prey
        '''
        raise NotImplementedError
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        