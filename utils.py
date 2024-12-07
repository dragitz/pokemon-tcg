import random
from classes import *




def fight(card1:PokemonCard, card2:PokemonCard):

    move:Move = card1.moves[0]
    card2.hp -= move.damage
    
    if card2.hp < 0:
        return 0
    
    return card2.hp
