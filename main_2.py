from backend.game_logic import Game
from backend.player import Player
from backend.player_stats import PlayerStats

from lupa import LuaRuntime


game = Game()

player1 = Player(0,"bot00",PlayerStats())
player2 = Player(1,"bot01",PlayerStats())

game.createPlayers(player1,player2)

game.MAX_SIMULATED_GAMES = 1000
game.playGame()



