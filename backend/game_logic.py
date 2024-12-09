import random
from .player import *
from .move import *
from .pokemon_card import *
from .enums import *

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


    
class Game:
    def __init__(self):
        self.game_id = 0
        
        self.rules = Rules()
        self.logic = GameLogic()

        self.PlayerTurn = 0
        self.TotalTurns = 0

        self.starting_player = 0

        self.Player1 = None
        self.Player2 = None

        self.turns = 0
        self.gameFinished = False

        self.GAMES = 0
        self.MAX_SIMULATED_GAMES = 1000
    
    def createPlayers(self, Player1:Player, Player2:Player):
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
                card = PokemonCard(q,False,0,random.choice([100,120,140,160,180,110,130,150,170,190,200,210,220,230,240]),moves)
                
                fakeDeck.append(card)

        return fakeDeck
        
    #####################################################

    def giveEnergy(self, player_id:int):
        pass
    def getActiveCard(self, player_id:int):
        pass

    def getBench(self, player_id:int):
        pass

    def getValidActions(self, player:Player):
        valid_actions = []

        # Always available
        valid_actions.append(Actions.END_TURN)

        # give energy to any card on the board
        if player.energy > 0 and (player.ActiveCard is not None or len(player.Bench) > 0):
            valid_actions.append(Actions.SET_ENERGY)
        
        # I don't think it's worth to have both options, as it could be considered as a waste of energy
        # eg, you just placed a pokemon in your active slot and waste energy to remove it?
        if player.ActiveCard == None:
            # check if player has basic pokemons that can be moved from either deck or bench
            if player.getBasicCardsAvailable() > 0:
                valid_actions.append(Actions.PLACE_ACTIVE)

        elif player.ActiveCard.energy >= player.ActiveCard.retreatCost:
            valid_actions.append(Actions.RETREAT)
        
        # check if player can place any pokemon in the bench, active pokemon must exist
        if player.ActiveCard is not None and len(player.Bench) < 3:
            # check if player has basic pokemons that can be moved from either deck or bench
            if player.getBasicCardsAvailable() > 0:
                valid_actions.append(Actions.PLACE_BENCH)
        
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
        self.Player1.Bench = [None, None, None]
        
        self.Player2.ActiveCard = None
        self.Player2.Bench = [None, None, None]

        self.TotalTurns = 0
        self.gameFinished = False

        self.turns = 0

    # The game will be played here
    def playGame(self):


        while self.GAMES < self.MAX_SIMULATED_GAMES:

            # Currently the reset function fully resets a deck to zero
            # note: unsure how to change the behavior of this function, will see in the future
            self.softReset()

            # Create temp deck
            # This is important until I code an actual deck (it's going to be a pain manually coding every card..)
            self.Player1.deck = self.createFakeDeck()
            self.Player2.deck = self.createFakeDeck()

            # shuffle player's decks
            self.Player1.deck = self.shuffleDeck(self.Player1.deck)
            self.Player2.deck = self.shuffleDeck(self.Player2.deck)

            # draw cards
            self.Player1.drawCard(self.rules.INITIAL_CARDS_DRAWN)
            self.Player2.drawCard(self.rules.INITIAL_CARDS_DRAWN)

            # who begins, track it, set to true 
            self.setInitialPlayer()

            while not self.gameFinished:
                self.turns += 1
                
                # set player for current turn
                if self.PlayerTurn == 1:
                    player = self.Player2
                    opponent = self.Player1
                else:
                    player = self.Player1
                    opponent = self.Player2
                
                # stats
                player.stats.total_turns += 1

                # give energy
                if self.TotalTurns >= 1:
                    player.energy = 1
                    player.drawCard(1)

                # check if top card needs to be placed on board slot 0 (main pokemon)
                if player.ActiveCard == None:
                    player.placeCard()

                # define active card
                active_card = player.ActiveCard
                active_card_rival = opponent.ActiveCard

                
                # Here we collect valid actions into an array, the ai will have to pick one
                player.valid_actions = self.getValidActions(player)


                # check if we have used our free energy
                # try attacking once card has been placed, given the turn id is greater than 0 (can not attack on the first turn) + can not attack empty slots
                if self.TotalTurns > 0 and player.Active is not None and opponent.Active is not None:
                    
                    valid_moves = active_card.getValidMoves()

                    # usually cards have moves, ensure this is true
                    # if false: ignore attacks
                    if len(valid_moves) > 0:

                        # here the ai should pick between a move
                        move = random.choice(active_card.moves)
    

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


