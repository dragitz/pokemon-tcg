import random
from .player import Player, Move
from .move import *
from .pokemon_card import *
from .enums import *

import lupa

class GameLogic:
    def __init__(self):
        self.variables = {"HEADS": 0}  # Store computed values like HEADS here

    def start_game(self):
        pass

    def attack(self, move, multiplier=1):
        #print(f"Attacking for {move.damage * multiplier} damage!")
        move._TotalDamage = move.damage * multiplier
        return move
        

    def heal(self, amount):
        print(f"Healing for {amount} health!")
    
    def apply_debuff(self, debuff_type):
        pass

    def draw_card(self,amount):
        print(f"Drawing {amount} card(s)")
    
    def throw_card(self, amount):
        print(f"Threw {amount} card(s) away")

    def place_card(self, card, slot):
        pass
    
    def retreat(self, retreat_amount):
        if retreat_amount >= 2:
            print("Pokemon retreated")
        else:
            print("Pokemon not retreated")

    def flip_coin(self, coin_flips):
        self.variables["HEADS"] = 0
        for i in range(0,coin_flips):
            if random.randint(0,1) == 1:
                self.variables["HEADS"] += 1
        #print(self.variables["HEADS"])

    def parse_logic(self, move_edit):

        logic = move_edit.logic
        lines = logic.strip().split("\n")
        for line in lines:
            line = line.strip()  # remove surrounding whitespace
            if not line:
                continue

            parts = line.split(" ")
            # checking the length of min 6 is a quick hack
            # cards do not vary much in term of ability, if more effects are required, they can be coded in a different line
            if len(parts) >= 6 and parts[0] == "IF" and parts[2] in {">=", "<=", "==", ">", "<"} and parts[4] == "THEN":
                
                
                variable = parts[1]
                operator = parts[2]
                threshold = int(parts[3])
                
                if variable in self.variables:
                    value = self.variables[variable]
                    condition_met = False
                    if operator == ">=" and value >= threshold:
                        condition_met = True
                    elif operator == "<=" and value <= threshold:
                        condition_met = True
                    elif operator == ">" and value > threshold:
                        condition_met = True
                    elif operator == "<" and value < threshold:
                        condition_met = True
                    elif operator == "==" and value == threshold:
                        condition_met = True

                    # 
                    if condition_met:
                        action = parts[5]
                        if "*" in action:
                            action, multiplier = action.split("*")
                            if multiplier.isdigit():
                                multiplier = int(multiplier)
                            elif multiplier in self.variables:
                                multiplier = self.variables[multiplier]
                            else:
                                raise ValueError(f"Unknown multiplier: {multiplier}")
                        else:
                            multiplier = 1

                        # execute the action
                        if action == "ATTACK":
                            move_edit = self.attack(move_edit, multiplier)
                        elif action == "HEAL":
                            self.heal(move_edit.damage * multiplier)
                        elif action == "RETREAT":
                            self.retreat(2)
                        elif action == "DRAW":
                            self.retreat(2)
        
        return move_edit


############################################################
############################################################
############################################################

    
class Game:
    def __init__(self):
        self.game_id = 0
        
        self.rules = Rules()
        self.logic = GameLogic()

        self.PlayerTurn = 0

        self.starting_player = 0

        self.Player1:Player = None
        self.Player2:Player = None

        self.turns = 0
        self.isSetup = True
        self.gameFinished = False

        self.GAMES = 0
        self.MAX_SIMULATED_GAMES = 1000
    
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

    def createFakeDeck(self):
        fakeDeck = []
        DECK_SIZE = self.rules.DECK_SIZE
        for q in range(0,DECK_SIZE):
                
                # How many coinfilps the move does
                TOTAL_COINFLIPS = random.randint(0,3) 
                # how many attacks per head are required in order to make an attack
                # this is just a test for the logic of the parser, i don't think there's such a card with similar conditions
                REQUIRED_HEADS = random.randint(0, TOTAL_COINFLIPS) if TOTAL_COINFLIPS > 0 else 0
                move = Move(
                    logic=f"""
                    IF HEADS >= {REQUIRED_HEADS} THEN ATTACK*HEADS
                    """,
                    move_type="Attack", # note: currently unused
                    energy_cost=random.randint(0,4),
                    damage=random.choice([20,25,30,35,45,50,55,60,70,80,90]),

                    coinflips=TOTAL_COINFLIPS,
                )
                moves = [move]
                #card = PokemonCard(q,False,0,random.choice([100,120,140,160,180,110,130,150,170,190,200,210,220,230,240]),moves)
                card = PokemonCard(q, False, Stages.BASIC, 100, move, PokemonType.GRASS)
                
                fakeDeck.append(card)

        return fakeDeck
        
    def createFakeDeck2(self):
        fakeDeck = []
        DECK_SIZE = self.rules.DECK_SIZE
        for q in range(0,DECK_SIZE):
                
                # How many coinfilps the move does
                TOTAL_COINFLIPS = random.randint(0,3) 
                move_1 = Move(
                    logic=f"""
                    function before_attack()
                        local heads = flip(1)
                        if heads == 1 then
                            damage = damage + 10
                        end
                    end
                    
                    """,
                    move_type="Attack", # note: currently unused
                    energy_cost=random.randint(0,4),
                    damage=100,

                    coinflips=TOTAL_COINFLIPS,
                )
                #card = PokemonCard(q,False,0,random.choice([100,120,140,160,180,110,130,150,170,190,200,210,220,230,240]),move_1)
                card = PokemonCard(q, False, Stages.BASIC, 100, move_1, PokemonType.GRASS)
                
                fakeDeck.append(card)

        return fakeDeck
        
    #####################################################

    def giveEnergy(self, player_id:int):
        pass
    def getActiveCard(self, player_id:int):
        pass

    def getBench(self, player_id:int):
        pass
    
    def executeAction(self, player:Player, actionId:int):
        

        

        # this will kill the infinite loop
        if actionId == Actions.END_TURN:
            player.end_turn = True
            
            if self.isSetup and self.turns > 1:
                self.isSetup = False
        print(f"Action: {actionId},   player: {player.name},   player.end_turn: {player.end_turn}")
        print("")

        # allow agent to pick a move
        if actionId == Actions.ATTACK:
            player.end_turn = True
            player.ActiveCard.move_1.execute_logic()
            

        

    def decideAction(self, player):
        # here we code the ai to choose something
        # right now it's pure randomness
        actionId = random.choice(player.valid_actions)        
        self.executeAction(player, actionId)
    
    def getValidActions(self, player:Player):
        free_bench_slots = 3
        if player.Bench_1 is not None: free_bench_slots -= 1
        if player.Bench_2 is not None: free_bench_slots -= 1
        if player.Bench_3 is not None: free_bench_slots -= 1

        valid_actions = []

        
        
        if self.isSetup:
            
            # During the setup phase, first card must be the Active pokemon
            # we already ensured player receives a playable pokemon at the start of the game (initial draw phase)
            if player.ActiveCard is None:
                return [Actions.PLACE_ACTIVE]
            
            # During the setup phase, after placing an active pokemon, if any other basic pokemon is available
            # allow agent to place them on the bench
            if player.ActiveCard is not None:
                valid_actions.append(Actions.END_TURN)
                if len(player.getBasicCardsAvailable()) > 0 and free_bench_slots < 3:
                    valid_actions.append(Actions.PLACE_BENCH)

                return valid_actions
        
        else:
        

            # Always available
            #valid_actions.append(Actions.END_TURN)

            # I don't think it's worth to have both options, as it could be considered as a waste of energy
            # eg, you just placed a pokemon in your active slot and waste energy to remove it?

            # Always ensure active card is present
            if player.ActiveCard == None:
                # check if player has basic pokemons that can be moved from either deck or bench
                if player.getBasicCardsAvailable() > 0:
                    valid_actions.append(Actions.PLACE_ACTIVE)
                else:
                    # knockout without backup
                    # ggs
                    return []
            else:

                if player.ActiveCard.energy >= player.ActiveCard.retreatCost:
                    valid_actions.append(Actions.RETREAT)
                
                # check if player can place any pokemon in the bench, active pokemon must exist
                if player.ActiveCard is not None and free_bench_slots < 3:
                    # check if player has basic pokemons that can be moved from either deck or bench
                    if player.getBasicCardsAvailable() > 0:
                        valid_actions.append(Actions.PLACE_BENCH)

                # give energy to any card on the board
                # note: this does not check which type of energy you have vs the pokemon type/move
                #       in this simulation energies are all neutral (for now)
                # note: still checking for the active card, even though at this point the player should have one (because of the above checks)
                if player.energy > 0 and (player.ActiveCard is not None or free_bench_slots > 0):
                        valid_actions.append(Actions.SET_ENERGY)
                        
                
                # check if active pokemon can attack ( this won't work )
                if player.ActiveCard is not None and not player.ActiveCard.attackDisabled and 1 == 2:
                    for move in player.ActiveCard.moves:
                        if player.ActiveCard.energy >= move.energy_cost:
                            # valid move has been found
                            valid_actions.append(Actions.ATTACK)
                            break
                
                # check if active pokemon can attack (test method)
                if player.ActiveCard is not None and not player.ActiveCard.attackDisabled:
                    if player.ActiveCard.energy >= player.ActiveCard.move_1.energy_cost:
                        # valid move has been found
                        valid_actions.append(Actions.ATTACK)

                # to be coded:
                """
                RETREAT     <-- swap position of your active pokemon with one in the bench
                            <-- can be done once per turn
                
                EVOLVE
                SURREND     <-- hard one to code, force a surrend if ai can't do anything?

                ATTACK      <-- attacking will end the turn

                USE_ITEM    <-- use any item as much as you have in your turn
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

        # setup players without resetting their data (stats)
        self.Player1.cards = []
        self.Player2.cards = []
        
        self.Player1.deck = []
        self.Player2.deck = []

        self.Player1.ActiveCard = None
        self.Player2.ActiveCard = None

        self.Player1.Bench_1 = None
        self.Player1.Bench_2 = None
        self.Player1.Bench_3 = None

        self.Player2.Bench_1 = None
        self.Player2.Bench_2 = None
        self.Player2.Bench_3 = None

        self.gameFinished = False

        self.turns = 0

    # The game will be played here
    def playGame(self):


        while self.GAMES < self.MAX_SIMULATED_GAMES:

            # Currently the reset function fully resets a deck to zero
            # note: unsure how to change the behavior of this function, will see in the future
            self.softReset()
            
            self.GAMES += 1

            # Create temp deck
            # This is important until I code an actual deck (it's going to be a pain manually coding every card..)
            self.Player1.deck = self.createFakeDeck2()
            self.Player2.deck = self.createFakeDeck2()

            # shuffle player's decks
            self.Player1.deck = self.shuffleDeck(self.Player1.deck)
            self.Player2.deck = self.shuffleDeck(self.Player2.deck)

            # draw cards + ensure a basic pokemon is drawn
            p1_reshuffles = 0
            valid_cards = []
            self.Player1.drawCard(self.rules.INITIAL_CARDS_DRAWN)
            print(len(self.Player1.cards))

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
            
            # extra card to the other player for each reshuffles
            self.Player1.drawCard(p2_reshuffles)
            self.Player2.drawCard(p1_reshuffles)


            # who begins, track it, set to true 
            self.setInitialPlayer()

            print(self.GAMES)
            while not self.gameFinished:
                
                # Current game turns
                self.turns += 1
                
                if self.isSetup and self.turns > 1:
                    self.isSetup = False
                
                # set player for current turn
                if self.PlayerTurn == 1:
                    player = self.Player2
                    opponent = self.Player1
                else:
                    player = self.Player1
                    opponent = self.Player2
                
                # allow the player to do an action
                player.end_turn = False

                # increase the total amount of turns a player has played
                player.stats.total_turns += 1

                # give energy
                if self.turns >= 1 and not self.isSetup:
                    player.energy = 1
                    player.drawCard(1)

                # check if top card needs to be placed on board slot 0 (main pokemon)
                if player.ActiveCard == None:
                    player.placeCard()

                # define active card
                active_card = player.ActiveCard
                active_card_rival = opponent.ActiveCard

                
                # Here we collect valid actions into an array, the ai will have to pick one
                while not player.end_turn:
                    player.valid_actions = self.getValidActions(player)
                    print(f"setup: {self.isSetup}   player.end_turn {player.end_turn}    turn: {self.turns}")

                    if len(player.valid_actions) < 1:
                        self.gameFinished = True
                        
                        player.stats.losses += 1
                        player.stats.knockout_without_backup += 1

                        opponent.stats.wins += 1
                        break

                    self.decideAction(player)
                    player.valid_actions = []

                # Change turn
                self.PlayerTurn = 1 - self.PlayerTurn


    

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


