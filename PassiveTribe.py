'''
Created on 26 avr. 2018

@author: nroux
'''
INITIAL_VITALITY = 10
class PassiveTribe(object):
    '''
    Represents the passive tribe (old people, wounded, children, and Protoss players.
    They consume food and produce nothing. They need to be fed each turn
    '''


    def __init__(self, game):
        '''
        Constructor
        '''
        self.game=game
        self.vitality = INITIAL_VITALITY
    def feed(self):
        '''
        Consume a certain quantity of food depending on the vitality of the tribe.
        If the tribe can't be fed, its vitality decreases.
        To be called each full turn.
        '''
        raise NotImplementedError