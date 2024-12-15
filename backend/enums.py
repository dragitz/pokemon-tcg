import random
from enum import Enum

class Actions(Enum):
    SET_ENERGY   = 0
    PLACE_ACTIVE = 1
    PLACE_BENCH  = 2
    RETREAT      = 3
    EVOLVE       = 4
    SURREND      = 5
    ATTACK       = 6
    USE_ITEM     = 7
    USE_SUPPORT  = 8
    END_TURN     = 9

class Debuffs(Enum):
    POISON    = 0
    SLEEP     = 1
    PARALYSIS = 2
    BURN      = 3
    CONFUSION = 4

class PokemonType(Enum):
    GRASS     = 0
    FIRE      = 1
    WATER     = 2
    LIGHTNING = 3
    PSYCHIC   = 4
    FIGHTING  = 5
    DARKNESS  = 6
    METAL     = 7
    DRAGON    = 8
    ITEM      = 9
    SUPPORTER = 10
    NONE      = 11

class Energy:
    def __init__(self, type:PokemonType, quantity=1):
        self.type = type
        self.quantity = quantity
        

















