from .player_stats import *
from .pokemon_card import *
from .enums import *
from .game_logic import GameLogic

import random

class Player:
    def __init__(self, id:int, name:str, stats:PlayerStats):
        self.id = id
        self.name = name
        self.stats = stats
        
        self.cards = []
        self.deck = []
        self.dead = []

        self.ActiveCard = PokemonCard()
        self.Bench = [None, None, None]

        self.energy = 0
        self.localGameTurnWins = 0

        self.valid_actions = []
        self.end_turn = False
    
    def placeCard(self):
        
        # Basic logic
        basic_in_hand = self.getBasicCardsInHand()
        item = random.choice(basic_in_hand)
        index = basic_in_hand.index(item)
        
        card = self.cards.pop(index)
        self.ActiveCard = card      # <-- hardcoded slot

        #print("card placed by player id: ",self.id)
    def shuffleDeck(self):
        deck = self.deck
        for i in range(len(deck)):
            rand = random.randint(0, len(deck)-1)
            deck[i], deck[rand] = deck[rand], deck[i]
        self.deck = deck
    
    def drawCard(self, amount:int):
        if amount <= 0:
            return
        
        deck_amount = len(self.deck)
        if deck_amount <= 0:
            print(self.name, "couldn't draw a card (this error can only be triggered if drawing a card was selected as a valid action when it wasn't)")
            print("valid_actions: ",self.valid_actions)
            return
        
        # draw a maximum of n cards if the size doesn't match
        for i in range(0,min(amount,len(self.deck))):
            self.cards.append(self.deck.pop(0))

    def getBasicCardsAvailable(self):
        valid = []
        
        for i in range(len(self.cards)):
            if self.cards[i].stage == Stages.BASIC:
                valid.append(self.cards[i])
        
        for i in range(len(self.Bench)):
            if self.Bench[i].stage == Stages.BASIC:
                valid.append(self.Bench[i])

        return valid
    
    def removeCard(self, id:int):
        self.cards.pop(0)
    
    class Move:
        def __init__(self, logic, move_type, energy_cost=1, damage=0, coinflips=0, debuffs=[]):
            self.logic = logic
            self.move_type = move_type
            
            self.damage = damage
            self.coinflips = coinflips
            self.debuffs = debuffs
            self.cards_drawn = 0
            self.energy_cost = energy_cost

            # do not edit
            self._TotalDamage = 0
            self._TotalHealing = 0


        def execute_logic(self, game_logic):
            move_data = game_logic.parse_logic(self)
            return move_data