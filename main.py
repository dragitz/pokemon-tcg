from backend.game_logic import Game
from backend.player import Player
from backend.player_stats import PlayerStats
from backend.enums import PlayerType

from lupa import LuaRuntime


game = Game()

player1 = Player(0,"bot00",PlayerStats(),PlayerType.BOT_RANDOM)
player2 = Player(1,"bot01",PlayerStats(),PlayerType.BOT_RANDOM)

game.createPlayers(player1,player2)

game.debugEvents = False
game.printStats = True

game.MAX_SIMULATED_GAMES = 100

game.playGame()



