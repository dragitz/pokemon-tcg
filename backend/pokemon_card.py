import random
from enum import Enum
from .enums import PokemonType

from lupa import LuaRuntime

class Stages(Enum):
    BASIC = "BASIC"
    STAGE_1 = "STAGE_1"
    STAGE_2 = "STAGE_2"
    #STAGE_3 = "STAGE_3"
    #STAGE_4 = "STAGE_4"
    
class CardType(Enum):
    MONSTER = 0
    ITEM    = 1

lua = LuaRuntime(unpack_returned_tuples=True)

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


    def execute_logic_old(self, game_logic):
        move_data = game_logic.parse_logic(self)
        return move_data
    
    def execute_logic(self):
        global lua
        lua_script = lua.eval(self.logic)

        
        lua_globals = lua.globals()
        lua_globals.damage = self.damage
        lua_globals.coinflips = self.coinflips

        def flip_coin(amount):
            heads = 0
            for i in range(amount):
                if random.randint(0,1) > 0:
                    heads += 1
            return heads
        
        # store function for coin clips
        lua_globals.flip = flip_coin

        # events
        lua_script.before_attack()   # coinflips
        lua_script.after_attack()    # debuffs, remove enrgy

        self._TotalDamage = lua_globals.damage
        print(f"Attack {self.damage}  -  self._TotalDamage {self._TotalDamage}")

class PokemonCard:
    def __init__(self, id:int, isEx:bool, stage:Stages, maxHp:int, move_1:Move, type:PokemonType, retreat_cost = 1, energy=0, asset_name = ""):

        self.id = id

        # Base data
        self.maxHp = maxHp
        self.hp    = self.maxHp
        self.health_bar = 100   # placeholder, will be updated upon taking damage

        self.moves = []
        self.moves.append(move_1) # temp fix

        # 
        self.move_1 = move_1
        #self.move_2 = move_2
        #self.ability = ability

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

