import random
from enum import Enum

class PlayerType(Enum):
    PLAYER      = 0
    BOT_RANDOM  = 1
    BOT_QAGENT  = 2

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
        

class TargetSlots(Enum):
    ACTIVE  = 0
    BENCH_1 = 1
    BENCH_2 = 2
    BENCH_3 = 3

# from https://bulbapedia.bulbagarden.net/wiki/Category:Cards_by_effect
class GameEffects(Enum):
    ATTACH_ENERGY      = 0
    CHANGE_ATTACK_COST = 1
    CHANGE_ORDER_OF_CARDS_IN_DECK = 2
    CHANGE_RETREAT_COST = 3
    CHANGE_DAMAGE_COUNTERS_ON_CONFUSED_POKEMON = 4
    DISCARD_ENERGY_FROM_OPPONENT_CARDS = 5
    DISCARD_FROM_DECK = 6
    DISCARD_FROM_HAND = 7
    DISCARD_TOOL = 8 # unsure about this one
    DISCARD_STADIUM = 9 # currently not present in pocket
    DRAW_CARD = 10
    EVOLVE_POKEMON = 11
    DEVOLVE_POKEMON = 12
    END_TURN = 13
    END_GAME = 14
    HEAL = 15
    HEAL_SPECIAL_CONDITIONAL = 16
    DAMAGE_CONDITION = 17
    ROCK_PAPER_SCISSORS = 18
    MOVE_CARD_INTO_DECK = 19
    MOVE_CARD_INTO_HAND = 20
    MOVE_DAMAGE_COUNTER = 21 # unsure
    MOVE_OPPONENT_POKEMON_WITH_ENERGY_INTO_DECK = 22 # not currently present in pocket
    MOVE_POKEMON_TO_BENCH = 23
    PREVENT_RETREAT = 24
    REVEAL_HAND = 25
    SWITCH_ACTIVE_POKEMON = 26
    # CARDS_WITH_DISCARD_COSTS = WTF is this?
    ATTACK_WHILE_ASLEEP = 27
    CHANGE_TYPE = 28
    COPY_ATTACK = 29
    ATTACK_BENCHED_POKEMON = 30
    ATTACK_SELF = 31
    ATTACK_DAMAGE_MULTIPLIER_ENERGY = 32
    ATTACK_DAMAGE_MULTIPLIER_BENCHED_AMOUNT = 33
    ATTACK_DAMAGE_MULTIPLIER_COIN_FLIPS = 34
    ATTACK_DAMAGE_NO_WEAKNESS_NO_RESISTANCE = 35
    ATTACK_DAMAGE_INCREASE_IF_SPECIAL_CONDITION = 36
    ATTACK_DAMAGE_ZERO_IF_TAILS = 37
    EVOLVE_ALLOWED_FIRST_TURN = 38
    GRANT_EXTRA_TURN = 39
    KILL_OPPONENT_POKEMON = 40
    PREVENT_DAMAGE = 41
    PREVENT_DRAWING_CARDS = 42
    PREVENT_SPECIFIC_ATTACK = 43
    PREVENT_ATTACK_NEXT_TURN = 44
    TRAINER_PLAYABLE_IF_NO_LEGAL_CARDS = 45
    TRAINER_RETURN_TO_PLAYER_HAND = 46




    













