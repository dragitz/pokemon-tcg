from .backend.game_logic import *

game = Game()

player1 = Player(0,"bot00",PlayerStats())
player2 = Player(1,"bot01",PlayerStats())

game.createPlayers(player1,player2)

