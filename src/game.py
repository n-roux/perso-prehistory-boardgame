'''
Created on 26 avr. 2018

@author: nroux
'''
import board.Board
import passive_tribe.PassiveTribe
import player.Player
import random

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
        self.group_event_pile = self.init_group_event_pile()
        self.board_event_pile = self.init_board_event_pile()
        self.shelter_event_pile = self.init_shelter_event_pile()
        
    def init_group_event_pile(self):
        '''
        Create a dictionnary of random events which emulates a tile pile.
        '''
        raise NotImplementedError    
    def init_board_event_pile(self):
        '''
        Create a dictionnary of random events which emulates a tile pile.
        '''
        raise NotImplementedError
    def init_shelter_vent_pile(self):
        '''
        Create a dictionnary of random events which emulates a tile pile.
        '''
        raise NotImplementedError
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
    def transition_phase(self):
        '''
        Called after all players have taken their turn.
        
        Rules : 
        Les joueurs décident d’un commun accord de passer en phase de transition à tout moment, ou alors lorsque tous les personnages se retrouvent à 0 PA.
        1) Lors de la phase de transition on remet au maximum la barre de PA de tous les personnages (les PA non dépensés ne sont pas cumulés). 
        2) On tire une carte évènement pour chaque groupe ou personnage en dehors de l’abri rocheux et on les résout successivement.
        3) Ensuite on finalise l’action de la carte abri rocheux en cours (vérification des conditions accomplies ou non et application des effets ou non) que l’on défausse et on tire une nouvelle carte évènement d’abri rocheux qui sera active pour la durée du tour suivant.
        4) Ensuite on défausse la carte évènement de plateau et on en pioche une nouvelle qui sera active pour le tour prochain (effet immédiat avant le début du tour avec effet persistant sur la durée du tour).
        5) Ensuite on paye le besoin en nourriture de la tribu passive de l’abri rocheux si possible ou on décrémente le marqueur de vitalité de la tribu d’autant que de nourriture non payée.
        6) La phase de transition prend fin et on avance le marqueur de tour de 1.
        Un nouveau tour commence.
        '''
        raise NotImplementedError
    
    def draw_in_pile(self, str_pile_type):
        '''
        Given a pile type which can be board, shelter, or group,
        an event key is drawn in the event dictionnaries emulating the piles
        '''
        if str_pile_type== "board":
            if len(self.board_event_pile)==0:
                self.board_event_pile = self.init_board_event_pile()
            pile = self.board_event_pile
        elif str_pile_type == "shelter":
            if len(self.shelter_event_pile)==0:
                self.shelter_event_pile = self.init_shelter_vent_pile()
                pile = self.shelter_event_pile
        else :
            if len(self.init_group_event_pile()) ==0:
                self.group_event_pile = self.init_group_event_pile()
                pile = self.group_event_pile
        event_key = random.choice(pile.keys())
        del pile[event_key]
        return event_key    
    
    def draw_all_group_events(self):
        '''
        For each group of Meeple, draw a random event and apply it
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
        