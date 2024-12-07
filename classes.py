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
    def __init__(self, id:int, isEx:bool, stage:int, maxHp:int, moves:dict):

        self.id = id

        self.isEx = isEx
        self.stage = stage  # [0,1,2,3]
        
        self.maxHp = maxHp
        self.hp    = self.maxHp
        
        self.type = ""
        self.status_effects = []
        self.moves = moves
        self.weakness = ""

        self.retreatCost = 1
        self.rarity = 0
    
    def applyDamage(self, amount:int):
        self.hp -= amount
        return self




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
    def __init__(self, logic, move_type, damage=0, coinflips=0, debuffs=[]):
        self.logic = logic
        self.move_type = move_type
        
        self.damage = damage
        self.coinflips = coinflips
        self.debuffs = debuffs
        self.cards_drawn = 0
        
        # do not edit
        self._TotalDamage = 0
        self._TotalHealing = 0


    def execute_logic(self, game_logic):
        move_data = game_logic.parse_logic(self)
        return move_data


class PlayerCard:
    def __init__(self):
        self.wins = 0
        self.losses = 0

        self.total_games = 0
        self.total_games_first = 0
        self.total_games_first_won = 0
        self.total_turns = 0
        
        self.gold_wins = 0
        self.silver_wins = 0

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




class Player:
    def __init__(self, id:int, name:str, stats:PlayerCard):
        self.id = id
        self.name = name
        self.stats = stats
        self.cards = []
        self.Terrain = [None, None, None, None]


        self.localGameTurnWins = 0
    
    def placeCard(self, id: int, slot: int):
        card = self.cards.pop(id)
        self.Terrain[slot] = card

        #print("card placed by player id: ",self.id)
    
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


