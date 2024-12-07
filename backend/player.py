from player_stats import *
import random

class Player:
    def __init__(self, id:int, name:str, stats:PlayerStats):
        self.id = id
        self.name = name
        self.stats = stats
        
        self.cards = []
        self.deck = []
        self.dead = []

        self.Terrain = [None, None, None, None]

        self.energy = 0
        self.localGameTurnWins = 0
    
    def placeCard(self):
        
        # Basic logic
        basic_in_hand = self.getBasicCardsInHand()
        item = random.choice(basic_in_hand)
        index = basic_in_hand.index(item)
        
        card = self.cards.pop(index)
        self.Terrain[0] = card      # <-- hardcoded slot

        #print("card placed by player id: ",self.id)
    def shuffleDeck(self):
        deck = self.deck
        for i in range(len(deck)):
            rand = random.randint(0, len(deck)-1)
            deck[i], deck[rand] = deck[rand], deck[i]
        self.deck = deck
    
    def drawCard(self, amount:int):
        deck_amount = len(self.deck)
        if deck_amount <= 0:
            print(self.name, "couldn't draw a card")
            return
        
        # draw a maximum of n cards if the size doesn't match
        for i in range(0,min(amount,len(self.deck))):
            self.cards.append(self.deck.pop(0))

    def getBasicCardsInHand(self):
        valid = []
        
        for i in range(len(self.cards)):
            if self.cards[i].isBasic:
                valid.append(self.cards[i])
        return valid
    
    def removeCard(self, id:int):
        self.cards.pop(0)