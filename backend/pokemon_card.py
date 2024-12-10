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



class Move:
    def __init__(self, before_attack, after_attack, move_type, energy_cost=1, damage=0, coinflips=0, debuffs=[]):
        
        self.move_type = move_type
        
        self.damage = damage
        self.coinflips = coinflips
        self.debuffs = debuffs
        self.cards_drawn = 0
        self.energy_cost = energy_cost

        # do not edit
        self._TotalDamage = 0
        self._TotalHealing = 0

        self.before_attack = before_attack
        self.after_attack = after_attack

    
    def execute_logic(self, player, opponent):
        lua = LuaRuntime()

        if self.before_attack == "": self.before_attack = "function() end"
        lua_script_before_attack = lua.eval(self.before_attack)

        if self.after_attack == "": self.after_attack = "function() end"
        lua_script_after_attack = lua.eval(self.after_attack)

        # Global properties that lua can access
        # eg: "lua_globals.damage" in lua will be "damage"
        lua_globals = lua.globals()
        lua_globals.damage = self.damage
        
        lua_globals.heads = 0
        for i in range(self.coinflips):
            if random.randint(0,1) > 0:
                lua_globals.heads += 1
        
        lua_globals.energy_removed = 0
        lua_globals.self_heal      = 0

        # execute both scripts here
        lua_script_before_attack()
        lua_script_after_attack()    # debuffs, remove enrgy

        self._TotalDamage = lua_globals.damage

        # simple damage calculation
        opponent.ActiveCard.hp -= self._TotalDamage
        opponent.ActiveCard.health_bar = max(opponent.ActiveCard.hp,1) / opponent.ActiveCard.maxHp * 100

        # update damage stats
        player.stats.total_damage_inflicted += self._TotalDamage
        opponent.stats.total_damage_received += self._TotalDamage
        
        #print(f"Attack {self.damage}  -  self._TotalDamage {self._TotalDamage}")

class PokemonCard:
    def __init__(self, id:int, isEx:bool, stage:Stages, maxHp:int, move_1:Move, type:PokemonType, retreat_cost = 2, energy=0, asset_name = ""):

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

