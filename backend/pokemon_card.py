import random
import re
from enum import Enum
from .enums import PokemonType


from lupa import LuaRuntime



class Stages(Enum):
    BASIC   = 1
    STAGE_1 = 2
    STAGE_2 = 3
    NONE    = 99
    #STAGE_3 = "STAGE_3"
    #STAGE_4 = "STAGE_4"
    
class CardType(Enum):
    MONSTER = 0
    ITEM    = 1
    NONE    = 99

class CategoryType(Enum):
    POKEMON = 0
    ITEM    = 1
    TRAINER = 2
    NONE    = 99


class Move:
    def __init__(self, before_attack, after_attack, activation_script, upon_turn_change, precondition, move_type, energy_cost=1, damage=0, coinflips=0, debuffs=[]):
        
        self.move_type = move_type
        
        self.damage = damage

        self.coinflips = coinflips
        self.debuffs = debuffs
        self.cards_drawn = 0
        self.energy_cost = energy_cost

        # do not edit
        self._TotalDamage = 0
        self._TotalHealing = 0

        self.upon_turn_change = upon_turn_change
        self.activation_script = activation_script
        self.before_attack = before_attack
        self.after_attack = after_attack

        self.precontition = precondition
        

    def switch_active_with_bench(player, bench_index):
        target_pokemon = player.Bench[bench_index]
        target_pokemon.energy, player.ActiveCard.energy = player.ActiveCard.energy, target_pokemon.energy
        target_pokemon.hp, player.ActiveCard.hp = player.ActiveCard.hp, target_pokemon.hp
        
        player.Bench[bench_index], player.ActiveCard = player.ActiveCard, target_pokemon

        return player
    
    def execute_logic(self, game, player, opponent):
        lua = LuaRuntime()
        if self.upon_turn_change == "": self.upon_turn_change = "function() end"
        lua_script_upon_turn_change = lua.eval(self.upon_turn_change)
            
        # mainly for cards that do not have any attacks
        # this has priority over the other before_attack and after_attack
        if self.activation_script == "": self.activation_script = "function() end"
        lua_script_activation_script = lua.eval(self.activation_script)

        if self.before_attack == "": self.before_attack = "function() end"
        lua_script_before_attack = lua.eval(self.before_attack)

        if self.after_attack == "": self.after_attack = "function() end"
        lua_script_after_attack = lua.eval(self.after_attack)

        

        # Global properties that lua can access
        # eg: "lua_globals.damage" in lua will be "damage"
        lua_globals = lua.globals()

        lua_globals.game = game
        lua_globals.player = player
        lua_globals.opponent = opponent

        lua_globals.damage = self.damage

        lua_globals.heads = 0
        for i in range(self.coinflips):
            if random.randint(0,1) > 0:
                lua_globals.heads += 1
        
        lua_globals.energy_removed = 0  # currently unused
        lua_globals.self_heal      = 0  # currently unused

        
        # execute scripts here
        lua_script_upon_turn_change()
        lua_script_activation_script()
        lua_script_before_attack()
        lua_script_after_attack()    # debuffs, remove enrgy

        self._TotalDamage = lua_globals.damage

        # simple damage calculation
        opponent.ActiveCard.hp -= self._TotalDamage
        opponent.ActiveCard.health_bar = max(opponent.ActiveCard.hp,1) / max(opponent.ActiveCard.maxHp,1) * 100

        # update damage stats
        player.stats.total_damage_inflicted += self._TotalDamage
        opponent.stats.total_damage_received += self._TotalDamage
        
        #print(f"Attack {self.damage}  -  self._TotalDamage {self._TotalDamage}")

class PokemonCard:
    def __init__(self, Category:CategoryType, name:str, maxHp:int, types, stage:Stages, attacks, retreatCost:int, evolveFrom:str, weaknesses:PokemonType, isEx:bool) :

        self.category = Category
        self.name = name.replace(" ","_")
        self.hp = maxHp
        self.maxHp = maxHp
        self.health_bar = 100   # placeholder, will be updated upon taking damage

        self.types = types
        self.stage = stage

        self.attacks = []
        for attack in attacks: # dev note: finish this
            energy_cost = len(attack["cost"])
            
            if "damage" in attack:
                damage = attack["damage"]
                damage = damage.replace("+", "")
                damage = int(damage.replace("x", ""))
            else:
                damage = 0
            
            # dev note: to be coded
            if "coinflips" in attack:
                coinflips = attack["coinflips"]
            else:
                coinflips = 0
            debuffs = []

            #self, before_attack, after_attack, activation_script, upon_turn_change, precondition, move_type, energy_cost=1, damage=0, coinflips=0, debuffs=[]

            move = Move(
                attack["before_attack"], 
                attack["after_attack"], 
                "",
                "",
                self.types[0], 
                energy_cost, 
                damage, 
                coinflips, 
                debuffs
                )
            self.attacks.append(move)

        self.retreatCost = retreatCost
        self.evolveFrom = evolveFrom
        self.weaknesses = weaknesses

        self.isEx = isEx

        # dynamic
        self.energy = 0
        self.placed_turn = 0
        
        self.attackDisabled = False

        # Other
        self.asset = "assets\images\\"+self.name+".png"
        #print(self.asset)

        
    
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


