from .player_stats import *
from .pokemon_card import *
from .enums import *

import random


class Player:
    def __init__(self, id:int, name:str, stats:PlayerStats, PType:PlayerType):
        self.id = id
        self.name = name
        self.stats = stats
        
        self.cards = []
        self.graveyard = []
        self.deck = []
        self.deck_original = []
        

        self.ActiveCard = None
        self.Bench = []

        self.end_turn = False

        self.energy = 0
        self.localGameTurnWins = 0

        self.valid_actions = []
        
        self.possible_evolutions = []

        self.PlayerType = PType
    
    def decide(self, options=[]):

        if self.PlayerType == PlayerType.BOT_RANDOM:
            return random.choice(options)
        
        # temp solution
        return random.choice(options)
        # dev note: implement qagent in the future and player inputs (will need a basic ui)
    
    def placeCard(self):
        
        # Basic logic
        basic_in_hand = self.getBasicCardsInHand()
        item = self.decide(basic_in_hand)
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

        for card in self.Bench:
            if card.stage == Stages.BASIC:
                valid_basic_bench.append(card)
        
        return valid_basic_bench

    def getBasicCardsAvailable(self):
        valid = self.getBasicCardsInHand()
        
        cards = self.getBasicCardsInBench()
        for card in cards:
            valid.append(card)
            
        
        return valid
    
    def removeCard(self, id:int):
        self.cards.pop(0)
    
    def printStats(self):

        name = self.name
        stats = self.stats

        print(name +" Stats:")

        print(" ","Wins: ",stats.wins)
        print(" ","knockout_without_backup: ",stats.knockout_without_backup)
        print(" ","deckouts: ",stats.deckouts)
        print(" ","total_evolutions: ",stats.total_evolutions)
        print(" ","total_damage_inflicted: ",stats.total_damage_inflicted)
        print(" ","total_damage_received: ",stats.total_damage_received)
        print(" ","total_coin_tosses: ",stats.total_coin_tosses)
        print(" ","total_coin_tosses_wins: ",stats.total_coin_tosses_wins)
        print(" ","gold_wins: ",stats.gold_wins)
        print(" ","silver_wins: ",stats.silver_wins)
        print(" ","total_monsters_killed: ",stats.total_monsters_killed)
        print(" ","total_monsters_lost: ",stats.total_monsters_lost)
        print(" ","total_turns: ",stats.total_turns)
