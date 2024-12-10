from enum import Enum
from .enums import PokemonType

class Stages(Enum):
    BASIC = "BASIC"
    STAGE_1 = "STAGE_1"
    STAGE_2 = "STAGE_2"
    #STAGE_3 = "STAGE_3"
    #STAGE_4 = "STAGE_4"
    
class CardType(Enum):
    MONSTER = 0
    ITEM    = 1

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

class PokemonCard:
    def __init__(self, id:int, isEx:bool, stage:Stages, maxHp:int, moves:dict, type:PokemonType, retreat_cost = 1, energy=0, asset_name = ""):

        self.id = id

        # Base data
        self.maxHp = maxHp
        self.hp    = self.maxHp
        self.health_bar = 100   # placeholder, will be updated upon taking damage

        self.moves = moves

        self.move_1 = move_1
        self.move_2 = move_2
        self.ability = ability

        self.isEx = isEx
        self.stage = stage
        
        self.type = type
        
        # Buffs/Debuffs

        # Dynamic data
        self.energy = energy
        self.placed_turn = 0
        self.retreatCost = retreat_cost
        self.attackDisabled = False

        # Other
        self.rarity = 0
        self.asset = "assets/"+asset_name

        
    
    def applyDamage(self, amount:int):
        self.hp -= amount
        self.health_bar = self.hp / self.maxHp * 100
        return self
    
    def getValidMoves(self):
        valid_moves = []
        for move in self.moves:
            if self.energy >= move.energy_cost:
                valid_moves.append(move)
        return valid_moves

