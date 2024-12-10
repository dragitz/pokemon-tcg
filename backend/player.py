from .player_stats import *
from .pokemon_card import *
from .enums import *

import random

class Player:
    def __init__(self, id:int, name:str, stats:PlayerStats):
        self.id = id
        self.name = name
        self.stats = stats
        
        self.cards = []
        self.deck = []
        self.dead = []

        self.ActiveCard = None

        self.Bench_1 = None
        self.Bench_2 = None
        self.Bench_3 = None

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

    def getBasicCardsInHand(self):
        valid = []
        for i in range(len(self.cards)):
            if self.cards[i].stage == Stages.BASIC:
                valid.append(self.cards[i])
        return valid
    
    def getBasicCardsInBench(self):
        valid_basic_bench = []
        if self.Bench_1 is not None and self.Bench_1.stage == Stages.BASIC:
            valid_basic_bench.append(self.Bench_1)
        if self.Bench_1 is not None and self.Bench_2.stage == Stages.BASIC:
            valid_basic_bench.append(self.Bench_2)
        if self.Bench_1 is not None and self.Bench_3.stage == Stages.BASIC:
            valid_basic_bench.append(self.Bench_3)
        
        return valid_basic_bench

    def getBasicCardsAvailable(self):
        valid = self.getBasicCardsInHand()
        
        cards = self.getBasicCardsInBench()
        for card in cards:
            valid.append(card)
            
        
        return valid
    
    def removeCard(self, id:int):
        self.cards.pop(0)
    
