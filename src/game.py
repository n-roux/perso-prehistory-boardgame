'''
Created on 26 avr. 2018

@author: nroux
'''
import board.Board
import passive_tribe.PassiveTribe
import player.Player


NORMAL = 0

class Game(object):
    '''
    Master class that handles all events not decided by players. An instance of this class is created to start a game, and it creates instances of all necessary components of a game
    '''


    def __init__(self, player_name_array, player_meeple_type_array, game_mode=0):
        '''
        Constructor
        '''
        self.player_count = len(player_name_array)
        self.player_array = []
        for player_id in range(self.player_count):
            self.player_array.append(player(game=self, player_id=player_id,
                                            player_name=player_name_array[player_id],
                                            player_meeple_type = player_meeple_type_array[player_id]))
                                     
        self.tiles = board(game=self)
        self.passive_tribe = passive_tribe(game=self)
        self.next_player = 0
        
    def check_victory_or_defeat(self):
        '''
        Function to call between each player turn to determine if players won or lost the game
        '''
        raise NotImplementedError
    def prompt_player(self, player_id):
        '''
        Invites a player to take his turn
        '''
        raise NotImplementedError
    def draw_events(self):
        '''
        Handles the random after a full round of player turns
        '''
        raise NotImplementedError
    def acknowledge_turn_end(self):
        '''
        To be called by a player instance after the end of is turn
        '''
        self.check_victory_or_defeat()
        self.next_player = (self.next_player +1) % self.player_count
        if self.next_player == 0:
            self.draw_events()
        self.prompt_player(player_id=self.next_player)
        