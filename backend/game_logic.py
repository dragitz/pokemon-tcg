import random
from player import *

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

        self.PlayerTurn = 0
        self.TotalTurns = 0

        self.starting_player = 0

        self.Player1 = None
        self.Player2 = None

        self.gameFinished = False
    
    def createGame(self):
        pass
    
    def createPlayers(self, Player1:Player, Player2:Player):
        self.Player1 = Player1
        self.Player2 = Player2

    # soft reset the game, keep player statistics and current deck (both can be edited)
    def resetGame(self):
        pass

    #####################################################
    def shuffleDeck(self):
        pass

    def drawCard(self, amount:int):
        pass
    
    def discardCard(self, player_id:int, slot:int):
        pass
    
    #####################################################

    def giveEnergy(self, player_id:int):
        pass
    
    def getActiveCard(self, player_id:int):
        pass

    def getBench(self, player_id:int):
        pass

    def getValidActions(self, player_id:int):
        pass

    def setInitialPlayer(self, forced_id:int):
        if not forced_id:
            self.PlayerTurn = forced_id
            self.starting_player = forced_id
        else:
            self.PlayerTurn = random.randint(0,1)
            self.starting_player = self.PlayerTurn
    
    # The game will be played here
    def playGame(self):
        pass
    

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
        self.INITIAL_CARDS_GIVEN = 5
        self.MAX_CARDS_IN_HAND = 10
