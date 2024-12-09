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


class PokemonCard:
    def __init__(self, id:int, isEx:bool, stage:Stages, maxHp:int, moves:dict, type:PokemonType, retreat_cost = 1, energy=0, asset_name = ""):

        self.id = id

        # Base data
        self.maxHp = maxHp
        self.hp    = self.maxHp
        self.health_bar = 100   # placeholder, will be updated upon taking damage

        self.moves = moves

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

