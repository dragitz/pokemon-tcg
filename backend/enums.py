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

class Energy:
    def __init__(self, type:PokemonType, quantity=1):
        self.type = type
        self.quantity = quantity
        

















