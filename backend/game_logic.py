import random
from .player import Player, Move
from .move import *
from .pokemon_card import *
from .enums import *

import lupa
import json
import os



############################################################
############################################################
############################################################

    
class Game:
    def __init__(self):
        self.game_id = 0
        
        self.rules = Rules()

        self.PlayerTurn = 0

        self.starting_player = 0

        self.Player1:Player = None
        self.Player2:Player = None

        self.turns = 0
        self.isSetup = True
        self.gameFinished = False

        self.GAMES = 0
        self.MAX_SIMULATED_GAMES = 10

        self.debugEvents = False
        self.printStats = True
    
    def createPlayers(self, Player1, Player2):
        if Player1 == None:
            print("Player1 is None")
            return
        
        if Player2 == None:
            print("Player2 is None")
            return
        
        self.Player1 = Player1
        self.Player2 = Player2
    
    def deletePlayers(self):
        self.Player1 = None
        self.Player2 = None
    
    #####################################################
    def shuffleDeck(self, deck):
        for i in range(len(deck)):
            rand = random.randint(0, len(deck)-1)
            deck[i], deck[rand] = deck[rand], deck[i]
        return deck
    
    def shuffleSimple(self, deck):
        return random.shuffle(deck)

    
    def discardCard(self, player_id:int, slot:int):
        pass
    
    # once I have a proper way to load a deck and a working card db, then I can load decks
    # for now I'm going to use randomized/hardcoded cards
    # see createFakeDeck() for a temp replacement
    def loadDeck(self):
        pass
    
    def pickRandomFile(self):
        # randomly load a card from the db
        folder = "assets/cards"
        all_files = os.listdir(folder)

        json_files = []
        for file in all_files:
            if file.endswith(".json"):
                json_files.append(file)
        
        random_file = random.choice(json_files)
        file_path = os.path.join(folder, random_file)
        return file_path
    
    # generate random decks
    def createFakeDeck3(self):
        fake_deck = []
        for q in range(0,self.rules.DECK_SIZE):
            file = self.pickRandomFile()
            
            with open(file) as json_file:
                data = json.load(json_file)
            
            # data of card
            if "category" not in data:
                print(f"Card: {file} does not contain category")
                return
            if "name" not in data:
                print(f"Card: {file} does not contain name")
                return

            Category = CategoryType.NONE
            
            
            if data["category"] == "Pokemon":
                Category = CategoryType.POKEMON
            elif data["category"] == "Item":
                Category = CategoryType.ITEM
            elif data["category"] == "Trainer":
                Category = CategoryType.TRAINER

            Name = data["name"]
            #print(Name, data["category"])
            
            if Category == CategoryType.POKEMON:
                maxHp = data["hp"]
                types = [CardType.NONE]
                if "types" in data:
                    types = data["types"]

                if data["stage"] == "Basic":
                    stage = Stages.BASIC
                elif data["stage"] == "Stage1":
                    stage = Stages.STAGE_1
                elif data["stage"] == "Stage2":
                    stage = Stages.STAGE_2
                else:
                    stage = data["stage"]
                    print(f"Unknown stage: {stage}")
                    return []
                
                # dev note: properly handle this in pokemon_card
                abilities = []
                if "abilities" in data:
                    for ability in data["abilities"]:
                        abilities.append(ability)
                
                attacks = []
                for attack in data["attacks"]:
                    attacks.append(attack)
                retreat = data["retreat"]
            else:
                maxHp = 0
                types = []
                stage = Stages.NONE
                abilities = []
                attacks = []
                retreat = 0

            evolveFrom = ""
            if "evolveFrom" in data:
                evolveFrom = data["evolveFrom"]

            weakness = PokemonType.NONE
            isHex = False

            card = PokemonCard(Category, Name, maxHp, types, stage, attacks, retreat, evolveFrom, weakness, isHex)
            fake_deck.append(card)
        
        return fake_deck

        
    #####################################################

    def _get_ally_pokemon(self,player:Player):
        pass
    

    def giveEnergy(self, player:Player):
        pokemons = [player.ActiveCard]
        
        for card in player.Bench:
            pokemons.append(card)
        
        # use brain functions to decide which pokemon should get energy
        # for now it's random
        pokemon = random.choice(pokemons)
        pokemon.energy += 1


    def placeActiveCard(self, player:Player):
        # Brain should decide
        # for now it's random

        # give priority to pokemons in the hand
        card = None
        cards = player.getBasicCardsInHand()
        
        if len(cards) > 0: 
            card = random.choice(cards)
            card_index = cards.index(card)
            player.ActiveCard = player.cards.pop(card_index)
            return
        
        cards = player.getBasicCardsInBench()
        if len(cards) > 0:
            card = random.choice(cards)
            card_index = cards.index(card)
            player.ActiveCard = player.Bench.pop(card_index)
            return

        print("placeActiveCard::This should not get hit, wtf?")
        return
        
    def placeHandCardOnBench(self, player:Player):
        card = None
        cards = player.getBasicCardsInHand()
        if len(cards) > 0:
            card = random.choice(cards)
            card_index = cards.index(card)
            player.Bench.append(player.cards.pop(card_index))
            return
        
        print(f"placeHandCardOnBench::This should not get hit, wtf? isSetup: {self.isSetup}")
        return

        



    def getBench(self, player:Player):
        pass
    

    def executeAction(self, player:Player, actionId:int, opponent:Player):
        
        # this will kill the infinite loop
        if actionId == Actions.END_TURN:
            player.end_turn = True
            return    
        
        #print(f"Action: {actionId},   player: {player.name},   player.end_turn: {player.end_turn}")
        if self.debugEvents:
            print(f"{player.name},   Action: {actionId}            turn: {self.turns}")
        

        if actionId == Actions.PLACE_ACTIVE:
            self.placeActiveCard(player)
            return

        if actionId == Actions.PLACE_BENCH:
            self.placeHandCardOnBench(player)
            return
        
        # note: must allow agent to pick a move
        if actionId == Actions.ATTACK:
            player.end_turn = True

            # dev note: this is a hardcoded action (only move 1)
            move = player.ActiveCard.attacks[0]
            move.execute_logic(player, opponent)
            #player.ActiveCard.move_1.execute_logic(player, opponent)

            # check if we killed the opponent's active pokemon
            if opponent.ActiveCard.hp <= 0:
                player.localGameTurnWins += 1
                opponent.ActiveCard = None
                if self.debugEvents:
                    print(f"Player: {player.name} has killed a pokemon!   Total wins: {player.localGameTurnWins}")
            return
        
        if actionId == Actions.SET_ENERGY:
            self.giveEnergy(player)
            player.energy = 0
            return


        

            

        

    def decideAction(self, player, opponent):
        # here we code the ai to choose something
        # right now it's pure randomness
        actionId = random.choice(player.valid_actions)        
        self.executeAction(player, actionId, opponent)
    
    def getValidActions(self, player:Player, opponent:Player):
        free_bench_slots = 3 - len(player.Bench)

        valid_actions = []
        
        # In any given situation, placing an active pokemon should be the top priority
        if player.ActiveCard is None:
            if len(player.getBasicCardsAvailable()) > 0:
                return [Actions.PLACE_ACTIVE]
            else:
                return []  # end game
        
        if self.isSetup:

            # During the setup, try to place at least 2 pokemons on the bench
            # else, end turn
            if len(player.getBasicCardsAvailable()) > 0 and free_bench_slots < 2:
                return [Actions.PLACE_BENCH]
            else:
                return [Actions.END_TURN]
        else:
        

            

            # try to ensure at least one pokemon is in the bench
            #if free_bench_slots == 3 and len(player.getBasicCardsInHand()) > 0:
            #    return [Actions.PLACE_BENCH]

            # give energy to any card on the board
            # note: this does not check which type of energy you have vs the pokemon type/move
            #       in this simulation energies are all neutral (for now)
            # note: still checking for the active card, even though at this point the player should have one (because of the above checks)
            if player.energy > 0 and (player.ActiveCard is not None or free_bench_slots > 0):
                    valid_actions.append(Actions.SET_ENERGY)
                    return [Actions.SET_ENERGY]

            # Always available
            valid_actions.append(Actions.END_TURN)

            # Swap active pokemon with one in the bench
            if player.ActiveCard.energy >= player.ActiveCard.retreatCost and free_bench_slots > 0:
                valid_actions.append(Actions.RETREAT)
            
            # check if player can place any pokemon in the bench
            # check if player has basic pokemons that can be moved from either deck or bench
            if free_bench_slots > 0 and len(player.getBasicCardsInHand()) > 0:
                valid_actions.append(Actions.PLACE_BENCH)


                    
            
            # check if active pokemon can attack (test method)
            # dev note: this is a WIP
            if not player.ActiveCard.attackDisabled and opponent.ActiveCard is not None and len(player.ActiveCard.attacks) > 0:
                move = player.ActiveCard.attacks[0]
                if player.ActiveCard.energy >= move.energy_cost:
                    # valid move has been found
                    valid_actions.append(Actions.ATTACK)
                    

            # to be coded:
            """
            RETREAT     <-- swap position of your active pokemon with one in the bench
                        <-- can be done once per turn
            
            EVOLVE      <-- cannot evolve a basic pokemon on the same turn it was placed
                        <-- has an impact on hp? kinda ? dunno
                        <-- keeps the energies
            SURREND     <-- hard one to code, force a surrend if ai can't do anything?

            ATTACK      <-- attacking will end the turn

            USE_ITEM    <-- use any item as much as you have in your turn (usable from turn 3)
            USE_SUPPORT <-- use one at most per turn
            USE_ABILITY <-- some are active, some are passive, it really depends LOL 
                            (i laugh because I'll have to suffer while coding every ability)
            """

        return valid_actions

    
        

    def setInitialPlayer(self):
        if self.rules.force_initial_player:
            self.PlayerTurn = 0
            self.starting_player = 0
        else:
            value:int = random.randint(0,1)
            self.PlayerTurn = value
            self.starting_player = value
    
    # soft reset the game, keep player statistics and current deck (both can be edited)
    def softReset(self):
        # reset scores
        self.Player1.localGameTurnWins = 0
        self.Player2.localGameTurnWins = 0

        #
        self.Player1.energy = 0
        self.Player2.energy = 0

        self.Player1.end_turn = False
        self.Player2.end_turn = False

        # setup players without resetting their data (stats)
        self.Player1.cards = []
        self.Player2.cards = []
        
        self.Player1.deck = []
        self.Player2.deck = []

        self.Player1.ActiveCard = None
        self.Player2.ActiveCard = None
        self.Player1.Bench = []
        self.Player2.Bench = []

        self.gameFinished = False
        self.isSetup = True
        self.turns = 0

    # The game will be played here
    def playGame(self):

        if self.debugEvents:
            print(f"Starting game: {self.GAMES}")
        
        while self.GAMES < self.MAX_SIMULATED_GAMES:

            # Currently the reset function fully resets a deck to zero
            # note: unsure how to change the behavior of this function, will see in the future
            self.softReset()
            
            self.GAMES += 1

            # Create temp deck
            if self.debugEvents:
                print(f"Creating decks")
            # This is important until I code an actual deck (it's going to be a pain manually coding every card..)
            self.Player1.deck = self.createFakeDeck3()
            self.Player2.deck = self.createFakeDeck3()

            if self.debugEvents:
                print(f"Shuffling decks")
            # shuffle player's decks
            self.Player1.deck = self.shuffleDeck(self.Player1.deck)
            self.Player2.deck = self.shuffleDeck(self.Player2.deck)

            if self.debugEvents:
                print(f"P1 Draw initial")
            # draw cards + ensure a basic pokemon is drawn
            p1_reshuffles = 0
            valid_cards = []
            self.Player1.drawCard(self.rules.INITIAL_CARDS_DRAWN)
            valid_cards = self.Player1.getBasicCardsAvailable()
            
            while len(valid_cards) == 0:
                p1_reshuffles += 1
                
                # put the cards in the hand back into the deck and shuffle it. then draw 7
                for card in self.Player1.cards:
                    self.Player1.deck.append(self.Player1.cards.pop(0))
                
                self.Player1.shuffleDeck()

                self.Player1.drawCard(7)
                valid_cards = self.Player1.getBasicCardsAvailable()
                if len(valid_cards) > 0:
                    break
                
            if self.debugEvents:
                print(f"P2 Draw initial")

            p2_reshuffles = 0
            valid_cards = []
            self.Player2.drawCard(self.rules.INITIAL_CARDS_DRAWN)
            valid_cards = self.Player2.getBasicCardsAvailable()
            while len(valid_cards) == 0:
                p2_reshuffles += 1
                
                # put the cards in the hand back into the deck and shuffle it. then draw 7
                for card in self.Player2.cards:
                    self.Player2.deck.append(self.Player2.cards.pop(0))
                self.Player2.shuffleDeck()

                self.Player2.drawCard(7)
                valid_cards = self.Player2.getBasicCardsAvailable()
                if len(valid_cards) > 0:
                    break
            if self.debugEvents:
                print(f"Drawing cards")

            # extra card to the other player for each reshuffles
            self.Player1.drawCard(p2_reshuffles)
            self.Player2.drawCard(p1_reshuffles)


            # who begins, track it, set to true 
            self.setInitialPlayer()
            if self.debugEvents:
                print(f"Setup done. init")

            while not self.gameFinished:
                
                # Current game turns
                self.turns += 1
                
                if self.isSetup and self.turns == 3:
                    self.isSetup = False
                
                # set player for current turn
                if self.PlayerTurn == 1:
                    player = self.Player2
                    opponent = self.Player1
                else:
                    player = self.Player1
                    opponent = self.Player2
                
                # force end game
                if self.turns > self.rules.maxTurns:
                    self.gameFinished = True
                    player.stats.losses += 1
                    opponent.stats.losses += 1
                    break
                
                # allow the player to do an action
                player.end_turn = False

                # increase the total amount of turns a player has played
                player.stats.total_turns += 1

                # check if current player doesn't have any card left to draw in the deck
                if len(player.deck) < 1:
                    self.gameFinished = True
                    
                    player.stats.losses += 1
                    player.stats.deckouts += 1

                    opponent.stats.wins += 1
                    break

                if self.turns >= 3:
                    player.drawCard(1)
                if self.turns >= 4:
                    player.energy = 1
                    
                    #print(f"{self.turns}")


                # define active card
                active_card = player.ActiveCard
                active_card_rival = opponent.ActiveCard

                
                # Here we collect valid actions into an array, the ai will have to pick one
                while not player.end_turn:
                    player.valid_actions = self.getValidActions(player, opponent)
                    #print(player.valid_actions)
                    #print(f"setup: {self.isSetup}   player.end_turn {player.end_turn}    turn: {self.turns}")

                    if len(player.valid_actions) < 1:
                        self.gameFinished = True
                        
                        player.stats.losses += 1
                        player.stats.knockout_without_backup += 1

                        opponent.stats.wins += 1
                        if self.debugEvents:
                            print(f"shitty loss {self.GAMES} by {player.name}")
                        break

                    self.decideAction(player, opponent)

                    # win condition check
                    if player.localGameTurnWins == 3:
                        self.gameFinished = True

                        player.stats.wins += 1
                        opponent.stats.losses += 1
                        if self.debugEvents:
                            print("")
                        break

                    player.valid_actions = []

                # Change turn
                self.PlayerTurn = 1 - self.PlayerTurn
        
        # print end game stats for both players
        if self.printStats:
            self.Player1.printStats()
            self.Player2.printStats()


    

class Rules:
    def __init__(self):
        self.disabledSlots = [] #0, 1, 2, 3
        self.disabledCardIds = []
        self.disabledCardTypes = []
        self.disabledCardStats = []
        self.isDrawingDisabled = False
        self.isEnergyDisabled = False
        self.isItemDisabled = False
        
        self.maxTurns = 30

        self.DECK_SIZE = 20
        self.INITIAL_CARDS_DRAWN = 5
        self.MAX_CARDS_IN_HAND = 10

        self.force_initial_player = False


