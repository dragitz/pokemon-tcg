import random
from enum import Enum

class Actions(Enum):
    SET_ENERGY   = 0
    PLACE_ACTIVE = 1
    PLACE_BENCH  = 2
    RETREAT      = 3
    SUBSTITUTE   = 4
    EVOLVE       = 5
    SURREND      = 6
    ATTACK       = 7
    USE_ITEM     = 8
    USE_SUPPORT  = 9
    END_TURN     = 10

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

class Energy:
    def __init__(self, type:PokemonType, quantity=1):
        self.type = type
        self.quantity = quantity
        

















