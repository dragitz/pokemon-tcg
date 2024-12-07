import random
from enum import Enum

class Debuffs(Enum):
    POISON = "Poison"
    SLEEP = "Sleep"
    PARALYSIS = "Paralysis"
    BURN = "Burn"
    CONFUSION = "Confusion"

class PokemonType(Enum):
    GRASS = "Grass"
    FIRE = "Fire"
    WATER = "Water"
    LIGHTNING = "Lightning"
    PSYCHIC = "Psychic"
    FIGHTING = "Fighting"
    DARKNESS = "Darkness"
    METAL = "Metal"
    DRAGON = "Dragon"
    ITEM = "Item"
    SUPPORTER = "Supporter"

class PokemonCard:
    def __init__(self, id:int, isEx:bool, stage:int, maxHp:int, moves:dict, energy=0):

        self.id = id

        self.isEx = isEx
        self.stage = stage  # [0,1,2,3]
        
        self.maxHp = maxHp
        self.hp    = self.maxHp
        
        self.type = ""
        self.status_effects = []
        self.moves = moves
        
        self.isBasic = True
        self.energy = energy
        self.weakness = ""

        self.retreatCost = 1
        self.rarity = 0
    
    def applyDamage(self, amount:int):
        self.hp -= amount
        return self
    
    def getValidMoves(self):
        valid_moves = []
        for move in self.moves:
            if self.energy >= move.energy_cost:
                valid_moves.append(move)
        return valid_moves




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


class PlayerStats:
    def __init__(self):
        self.wins = 0
        self.losses = 0

        self.total_games = 0
        self.total_games_first = 0
        self.total_games_first_won = 0
        self.total_turns = 0
        
        self.gold_wins = 0
        self.silver_wins = 0
        self.bronze_wins = 0

        self.total_damage_inflicted = 0
        self.total_damage_received = 0
        self.total_healing_done = 0
        self.total_coin_tosses = 0
        self.total_coin_tosses_wins = 0

        self.total_monsters_placed = 0
        self.total_monsters_lost = 0
        self.total_monsters_killed = 0

        self.total_ex_killed = 0
        self.total_ex_lost = 0

        self.total_energy_placed = 0
        self.total_items_used = 0

        self.games_turns = []



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


class Board:
    def __init__(self):
        self.rules = Rules()

        self.PlayerTurn = 0
        self.TotalTurns = 0

        self.Player1 = None
        self.Player2 = None
    
    def spawnPlayers(self, Player1:Player, Player2:Player):
        self.Player1 = Player1
        self.Player2 = Player2


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


