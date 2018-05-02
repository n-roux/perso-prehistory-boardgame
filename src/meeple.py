'''
Created on 26 avr. 2018

@author: nroux
'''
from random import randint




class Meeple(object):
    '''
    Abstract class handling all the basic actions that can be performed by all different Meeple classes.
    Classes that have bonuses to certain actions will override parent method
    '''
    # Static attribute
    max_action_point = 6
    def __init__(self, player):
        '''
        Constructor
        '''
        self.player = player
        # Starting tile
        self.position = player.game.tiles[0]
        self.equipment = []
        self.action_point_count = Meeple.max_action_point
        self.major_bleeding_last_move_done = False
        self.group = self # we can consider a lone meeple is a group, but I'm not sure
        self.is_minor_bleeding = False
        self.is_major_bleeding = False
        self.is_handicapped = False
        self.is_feverish = False
        
    def rollD6(self):
        '''
        Returns the result of a D6 roll
        '''
        return randint(1,6)
    def roll2D6(self):
        '''
        Returns the result of the sum of two D6 rolls
        '''
        return self.rollD6()+self.rollD6()
    def refill_action_points(self):
        '''
        Restores the AP of a Meeple. To be called by the player for all his meeples after his turn.
        Rules :  
        L’état « fièvre » perdure jusqu’à la fin de la prochaine phase de transition.
        Un personnage avec ce statut en phase de transition ne récupère que 2PA. 
        S’il passe la phase de transition dans une zone avec un foyer il récupère 4PA.
        '''
        # Check fever status
        if self.is_feverish:
            # Check if home on Meeple tile
            if self.position.has_home_POI:
                self.action_point_count = max(Meeple.max_action_point, self.action_point_count + 4)
            else:
                self.action_point_count = max(Meeple.max_action_point, self.action_point_count + 2)
        # Meeple doesn't have fever
        else :
            self.action_point_count = Meeple.max_action_point
            
    def is_healthy(self):
        '''
        Returns True if the Meeple condition is HEALTHY, False Otherwise
        '''
        return not(self.is_bleeding() or self.is_handicapped or self.is_feverish)
    
    def is_bleeding(self):
        '''
        Check if meeple has any bleeding condition
        Note : useful when the Meeple is moving into a zone to attract predators
        '''
        return self.is_minor_bleeding or self.is_major_bleeding
    def dies(self):
        '''
        Kills the Meeple, and remove it from the board and game. 
        Its equipment is dropped on the ground
        It leave its group
        '''
        raise NotImplementedError
        
    def can_single_action(self):
        '''
        Check if the player had enough AP to perform a single action (cost is 1 by default)
        '''
        if self.is_dead(): return False
        if self.is_feverish() and self.action_point_count < 2 : return False
        return self.action_point_count >= 1
    
    def pay_single_action_AP_cost(self):
        '''
        Pays the action cost of a non-free single action (cost is 1 by default).
        This function should never be called without calling self.can_single_action() first !!
        '''
        action_cost = 1
        will_die = False
        if self.major_bleeding_last_move_done:
            # If a Meeple uses more than one AP when heavily bleeding, its second action causes him to die.
            will_die = True
        if self.is_feverish :
            # Fever increases each action cost
            action_cost += 1
        if self.is_major_bleeding :
            # The Meeple cannot do any more action without dying
            self.major_bleeding_last_move_done = True
        # Action price is paid.
        self.action_point_count -= action_cost
        if will_die:
            self.dies()  

    def action_move(self, direction):
        '''
        Move from the Meeple position to an ADJACENT tile in a direction (NE, EAST, SE, SW, WEST, NW).
        Cost is 1 AP, unless Meeple has conditions
        
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            WARNING : @Hadrien n'est pas tout à fait fixé sur le board (est-ce qu'il y aura des bords ou pas). Ne pas implémenter.
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Notes : 
        . Encounters are to be resolved in this function, using the encounter table of the Tile class
        . If the adjacent Tile does'nt exist (has not been revealed), the board method add_tile() is called
        
        Rules : 
        L’action de se déplacer coûte 1PA.
        Elle permet au personnage ou au groupe réalisant l’action de se déplacer sur une zone adjacente.
        Cette action entraine obligatoirement un jet de rencontre du fait de l’entrée dans une zone. 
        On se réfère au tableau de rencontre et d’évènement d’entrée de zone pour gérer la rencontre. 
        '''
        raise NotImplementedError
    def action_explore(self):
        '''
        Perform the Explore action.
        Cost is 1 AP, unless Meeple has conditions.
        Rules : 
        L’action d’exploration coûte 1PA. Elle permet de révéler la présence ou non d’un lieu d’intérêt dans la zone explorée.
        Quand un personnage ou un groupe réalise l’action d’exploration sur une zone on tire les dés et on se reporte au tableau d’exploration des zones.
        Quand une zone a été explorée avec succès on place le marqueur d’exploration sur celle-ci et le résultat obtenu est définitif, elle ne peut être explorée une seconde fois. (Si l’exploration est un succès et ne donne rien, la zone ne présente pas de lieu d’intérêt pour toute la partie.)

        '''
        raise NotImplementedError
    def action_hunt(self):
        '''
        Performs the hunt action.
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            WARNING : @Hadrien va refondre le système de chasse. Ne pas implémenter
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Rules : 
        Action de chasse : dans une zone un personnage ou un groupe peut chasser pour une action (une action par personnage dans le cas d’un groupe).
        Il lance les dés et se réfère au tableau de rencontre de zone.
        Si c’est un pisteur il ne lance pas les dés et choisit dans le tableau le gibier rencontré.
        Une fois le gibier rencontré, si c’est un prédateur, les joueurs lancent également leur(s) dé(s) de nombre (cf colonne « éléments récoltables » dans le tableau de la faune).
        Le groupe ou le personnage qui fait l’action de chasse cumule sa valeur de combat totale et la compare aux animaux rencontrés. Les proies et les proies dangereuses sont en troupeaux ou harde, leur nombre est donc considéré illimité. Les chasseurs peuvent en tuer autant que de multiples nécessaires à la valeur de combat de l’animal  pour attendre la valeur de combat du groupe de chasse. Dans le cas des proies dangereuses le même système s’applique. En revanche si aucun animal n’est tué dans le cas des proies dangereuses, le groupe de chasse doit fuir pour 1PA par personnage. Si un ou des personnages n’ont pas les PA nécessaires pour fuir ils sont tués. Dans le cas des prédateurs, si la valeur du groupe de chasse est supérieure au groupe de prédateur, ce dernier fuit, dans le cas contraire, le groupe de chasse doit fuir pour 1PA et un membre du groupe est dévoré, choisit en priorité dans cet ordre : TOUS les personnages sans PA restant puis un personnage dans cet ordre de choix : doyens puis chamans puis au choix des joueurs. Pour appliquer la fuite les personnages choisissent eux-mêmes leur zone de repli sur les zones adjacentes (ils peuvent donc se séparer). Ces entrées de zone provoquent une action d’entrée de zone : rencontre et évènements à résoudre immédiatement. 
        Exemple : A, B, C et D chassent. Aucun pisteur n’est parmi eux, ils lancent donc les dés. Ils tombent sur 3 Lions de valeur de combat de 12.
        Sans équipement particulier ils ont une valeur de combat de 4. Ils fuient tous en payant 1PA.
        A et B se replient en forêt où ils ne rencontrent rien à l’entrée de la zone. C et D décident de se replier en Colline.
        A l’entrée de zone ils jouent de malchance et rencontrent à nouveau un groupe de 4 lions. D n’a plus de PA et est tué.
        C dépense 1PA pour fuir, son repli est automatiquement effectué dans la zone d’où il vient, là où la chasse a été ratée.
        Ce repli ne provoque pas de jet de rencontre et C fini son déplacement dans la zone initiale de chasse.
        '''
        raise NotImplementedError # SEE WARNING ABOVE
        
    def action_gather(self):
        '''
        Performs the gather action.
        Cost is 1AP unless the Meeple has conditions.
        
        Rules : L’action « récolter » coûte 1PA. Dans une zone elle permet de trouver automatiquement une unité de nourriture de type « fruits et céréales».
        Si un gisement de silex est présent dans la zone, le joueur contrôlant le personnage réalisant l’action peut choisir entre une unité de nourriture ou une unité de silex.
        Si le personnage réalisant l’action est un chaman ou un fourrageur il a également la possibilité de chercher des plantes médicinales.
        Dans ce cas le joueur lance un dé et se réfère au tableau de trouvaille des plantes médicinale par zone en fonction de la zone où il se trouve.
        '''
        raise NotImplementedError
    def action_craft(self, crafted_item_id):
        '''
        Performs the Craft action.
        Cost is 1AP unless the Meeple has conditions.
        
        Rules : 
        L’action de fabriquer un objet ou un matériau raffiné coûte 1PA.
        Pour savoir quoi fabriquer les joueurs peuvent se référer au tableau de l’artisanat.
        Chaque fabrication coûte 1PA mais plusieurs d’entre elles nécessite des prérequis (matériau de base, présence d’un feu etc….)
        Certaines fabrications sont des réussites automatiques, d’autre sont soumises à des jets de dés.
        '''
        raise NotImplementedError
    def action_create_home(self):
        '''
        Add a home marker to the current Meeple position.
        Homes provide protection for some transition phase events, and allow Meeple to recover faster.
        Cost is 1AP unless Meeple has conditions.
        
        @Hadrien: Combien de temps restent les foyers ? Y'a des matériaux pour le faire ?
        '''
        raise NotImplementedError
    def action_fire(self):
        '''
        Add a fire marker to the current Meeple position. 
        Calls the Craft method, but removes the item from the Meeple inventory immediatly 
        '''
        raise NotImplementedError
    def join_group(self, Group):
        '''
        Join an existing group.
        '''
        raise NotImplementedError
    def leave_group(self):
        '''
        Leave current Group
        '''
        raise NotImplementedError
    def create_group(self, Meeple):
        '''
        Create a Group
        '''
        raise NotImplementedError
class Group(object):
    '''
    Rules : 
    
    Un groupe est formé par l’association de plusieurs personnages sur une même zone et accomplissant une action commune.
    Entrer ou quitter un groupe est une action gratuite. Pour entrer dans un groupe le personnage doit se trouver sur la même zone que le groupe.
    Quand un personnage quitte le groupe il reste sur la même zone. Cette notion permet de définir quels évènements s’appliquent à quels personnages.
    Un groupe concerné par un évènement implique que les personnages du groupe ont réalisés une action, cette action a donc été simultanée à tous les membres et le coût éventuel en PA a donc été payé simultanément par tous les personnages concernés.
    '''

    
    def __init__(self, new_member):
        '''
        Constructor
        '''
        self.members = [new_member]
        
    def invite_member(self, new_member):
        '''
        Add a new member to the group
        '''
        if not(new_member in self.members) and new_member.group != new_member:
            self.members.append(new_member)
            new_member.group = self
        else:
            print("Error : target meeple already in a group ! ")
    def can_single_action(self):
        '''
        Check if ALL the members of the group can perform a 1-AP action 
        '''
        raise NotImplementedError
    def action_move(self, direction):
        '''
        All group members perform the move action.
        Only one encounter happens.
        '''       
        raise NotImplementedError
    def action_explore(self):
        '''
        All group members perform the explore action.
        Only useful to fight a cave bear ?
        '''
        raise NotImplementedError
    def action_hunt(self):
        '''
        All group members perform the hunt action.
        Only one (group of) animal is encountered, but all capacities can be used
        ''' 
        raise NotImplementedError
    def join_group(self, Group):
        '''
        Merges two group together. The group that calls this method is destroyed, and the called group gets bigger
        '''
        raise NotImplementedError
    
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        