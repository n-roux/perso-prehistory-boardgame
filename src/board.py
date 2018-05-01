'''
Created on 26 avr. 2018

@author: nroux
'''
from random import randint

NOTHING = 0
MAMMOUTH = 1
WOOLY_RHINOCEROS = 2
MEGACEROS = 3
AUROCH = 4
REINDEER = 5 # Renne
HORSE = 6
BISON = 7
OVIBOS = 8
CAVE_LION = 9
HYENA = 10
CAVE_BEAR = 11
DEER = 12 # Cerf
IBEX = 13 # Bouquetin
D6LION = 14
D6HYENA = 15 # TWO D6 !!
MINOR_OPEN_WOUND = 16
MINOR_WOUND = 17
HUNTING_GROUND = 18
SILEX = 19
CAVITY = 20
FEVER_PLANT = 21
COAGULATION_PLANT = 22
CATAPLASM_PLANT = 23



class Board(object):
    '''
    Represents the revealed world map. Is a collection of Tile instances.
    '''


    def __init__(self, game):
        '''
        Constructor
        '''
        self.game = game
        first_tile = Hills(game=self, tile_id = 0)
        first_tile.has_shelter = True
        first_tile.is_explored = True
        self.tiles = [first_tile]
        self.tile_count = 1
        
    def add_random_tile(self, old_tile, direction):
        '''
        Determine the type of the next tile, and add it to the Board
        '''       
        # Handling tile type
        tile_type = self.determine_tile_type()
        if tile_type == 0 : new_tile = Hills(game=self, tile_id=self.tile_count+1)
        elif tile_type == 1 :  new_tile = Forest(game=self, tile_id=self.tile_count+1)
        elif tile_type == 2 :  new_tile = River(game=self, tile_id=self.tile_count+1)
        elif tile_type == 3 :  new_tile = Plain(game=self, tile_id=self.tile_count+1)
        # Handling adjacency
        old_tile.direction = new_tile
        if direction == "NW":
            new_tile.SW = old_tile.W
            new_tile.EAST = old_tile.NE
            new_tile.SE = old_tile
        elif direction == "NE":
            new_tile.SE = old_tile.EAST
            new_tile.WEST = old_tile.NW
            new_tile.SW = old_tile
        elif direction == "EAST":
            new_tile.NW = old_tile.NE
            new_tile.SW = old_tile.SW
            new_tile.WEST = old_tile    
        elif direction == "SE":
            new_tile.NE = old_tile.EAST
            new_tile.WEST = old_tile.SW
            new_tile.NW = old_tile
        elif direction == "SW":
            new_tile.EAST = old_tile.SE
            new_tile.NW = old_tile.WEST
            new_tile.NE = old_tile
        elif direction == "WEST":
            new_tile.SE = old_tile.SW
            new_tile.NE = old_tile.NW
            new_tile.EAST = old_tile
        # TODO : Add it to the GUI
        self.tiles.append(new_tile)
        self.tile_count += 1
        
    def determine_tile_type(self): 
        '''
        Determine wether the Tile instance is a Forest, River, Plain, or Hills.
        TODO : Smarter randomness. Here we consider an infinite supply of tiles
        '''
        return randint(0,3)

class Tile(object):
    '''
    An abstract class to gather all the methods common to the four types of tiles
    '''


    def __init__(self, game, tile_id, NW=None, NE=None, EAST=None, SE=None, SW=None, WEST=None):
        '''
        Constructor
        '''
        self.game = game
        self.tile_id = tile_id
        self.NW = NW
        self.NE = NE
        self.EAST = EAST
        self.SE = SE
        self.SW = SW
        self.WEST = WEST
        self.is_explored = False
        self.has_home_POI = False
        
    def explore_tile(self):
        '''
        Check the Tile exploration table, and mark the Tile instance as explored
        '''
        raise NotImplementedError

class Forest(Tile):
    '''
    A bunch of trees. On a more serious note, this subclass doesn't have any overriding method
    '''
    # Static class variable (e.g. call the variable Forest.hunt_table)
    hunt_table = [CAVE_BEAR,CAVE_BEAR,AUROCH,DEER,NOTHING,NOTHING,NOTHING,DEER,NOTHING,NOTHING]
    encounter_table = [CAVE_BEAR, MINOR_OPEN_WOUND, NOTHING,NOTHING,NOTHING,NOTHING,NOTHING,NOTHING,NOTHING,AUROCH, CAVE_BEAR]
    exploration_table = [NOTHING, NOTHING,NOTHING, NOTHING, NOTHING, NOTHING]
    plant_table = [COAGULATION_PLANT, COAGULATION_PLANT, FEVER_PLANT, NOTHING, NOTHING, NOTHING]
    
class Hills(Tile):
    '''
    classdocs
    '''
    hunt_table = [CAVE_BEAR, CAVE_LION, IBEX,REINDEER,NOTHING,NOTHING,NOTHING,NOTHING,IBEX,NOTHING,NOTHING]
    encounter_table = [D6LION, MINOR_WOUND, NOTHING,NOTHING,NOTHING,NOTHING,NOTHING,NOTHING,NOTHING,CAVE_BEAR, D6HYENA]
    exploration_table = [SILEX, NOTHING, CAVITY, NOTHING, NOTHING, HUNTING_GROUND]
    plant_table = [COAGULATION_PLANT, FEVER_PLANT, FEVER_PLANT, NOTHING, NOTHING, NOTHING]

    def __init__(self, game, tile_id, NW=None, NE=None, EAST=None, SE=None, SW=None, WEST=None):
        '''
        Constructor
        '''
        self.super(Hills, self, game, tile_id, NW=None, NE=None,
                   EAST=None, SE=None, SW=None, WEST=None).__init__()
        self.has_silex_POI = False
        self.has_hunting_POI = False
        self.has_cavity_POI = False
        self.has_cave_POI = False
        self.has_shelter_POI = False
    def explore_tile(self):
        '''
        Override super method because it can add a POI
        TODO : Handles double exploration with cave
        '''
        Tile.explore_tile(self)
        raise NotImplementedError
    def explore_cavity(self):
        raise NotImplementedError    
        
        
class River(Tile):
    '''
    classdocs
    '''
    hunt_table = [CAVE_LION,MAMMOUTH, AUROCH,BISON,NOTHING,NOTHING,NOTHING,NOTHING,NOTHING,OVIBOS, HYENA]
    encounter_table = [D6LION, AUROCH, CAVE_BEAR, NOTHING, NOTHING, NOTHING, NOTHING, NOTHING, NOTHING, BISON, MAMMOUTH]
    exploration_table = [HUNTING_GROUND, NOTHING, NOTHING, NOTHING, NOTHING, NOTHING]
    plant_table = [CATAPLASM_PLANT, CATAPLASM_PLANT, FEVER_PLANT, COAGULATION_PLANT, NOTHING, NOTHING]


    def __init__(self, game, tile_id, NW=None, NE=None, EAST=None, SE=None, SW=None, WEST=None):
        '''
        Constructor
        '''
        self.super(River, self, game, tile_id, NW=None, NE=None,
                   EAST=None, SE=None, SW=None, WEST=None).__init__()
        self.has_hunting_POI = False
    def explore_tile(self):
        Tile.explore_tile(self)
        raise NotImplementedError
    
class Plain(Tile):
    '''
    classdocs
    '''
    hunt_table = [MAMMOUTH,WOOLY_RHINOCEROS, MEGACEROS, AUROCH, REINDEER, REINDEER, HORSE, BISON, OVIBOS, CAVE_LION, HYENA]
    encounter_table = [D6LION, AUROCH, CAVE_BEAR, NOTHING, NOTHING,NOTHING,NOTHING,NOTHING,NOTHING, BISON, MAMMOUTH]
    exploration_table = [HUNTING_GROUND, NOTHING, NOTHING, NOTHING, NOTHING, SILEX]
    plant_table = [FEVER_PLANT, COAGULATION_PLANT, NOTHING, NOTHING, NOTHING, NOTHING]

    def __init__(self, game, tile_id, NW=None, NE=None, EAST=None, SE=None, SW=None, WEST=None):
        '''
        Constructor
        '''
        self.super(Plain, self, game, tile_id, NW=None, NE=None,
                   EAST=None, SE=None, SW=None, WEST=None).__init__()
        self.has_silex_POI = False
        self.has_hunting_POI = False
        
    def explore_tile(self):
        Tile.explore_tile(self)
        raise NotImplementedError    
        
