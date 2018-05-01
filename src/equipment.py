'''
Created on 26 avr. 2018

@author: nroux
'''

class Item(object):
    '''
    Waiting for the rules development
    '''


    def __init__(self, Tile, item_id):
        '''
        Constructor
        '''
        self.position = Tile
        self.id = item_id


class Crafted(Item):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    def get_bonus(self):
        raise NotImplementedError

class Food(Item):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    def consume(self):
        '''
        Feed a passive tribe member. Not sure this function will be useful
        '''
        raise NotImplementedError
class Material(Item):
    '''
    Materials are used by a meeple to craft a Crafted item.
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        