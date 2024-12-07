"""
Types:
Pokemon TCG Pocket - Grass
Pokemon TCG Pocket - Fire
Pokemon TCG Pocket - Water
Pokemon TCG Pocket - Lightning
Pokemon TCG Pocket - Psychic
Pokemon TCG Pocket - Fighting
Pokemon TCG Pocket - Darkness
Pokemon TCG Pocket - Metal
Pokemon TCG Pocket - Dragon
Pokemon TCG Pocket - Item
Pokemon TCG Pocket - Supporter
"""

"""
For the scraper:
    download the images
    process the data into a json file (will later use sqlite)
    apply 99999 to data when there are errors (to later be found with ctl+f)

Verify the data, ensure all pokemons have a type, valid health, all slots filled
"""

"""
For the battle system:
    Build something simplistic.
    Keep in mind, the board can be manipulated by the dev who codes the bot
        * toggle slots (board rules)
        * toggle the usage of a card by id, type or stat (board rules)
        * toggle card drawing (board rules)
        * toggle 
"""
"""
For the logic:
    choose if it's better to start coding a card's logic, or handling it in the arena with some api endpoints

    ##
    pokemons may have more than one attack, each attack may or may not use a coin flip mechanic
    game must handle number of coin flips
    ##
    knowing that we could start by creating a system that handles how many coin flips.

    or we can create a player data page, like the lice driver in mario kart that tracs data about the player.
    we collect a bunch of ideas of things we want to collect, and we build the system on top of it

"""

#class AttackId

import random
import time
from utils import *

MAX_SIMULATED_GAMES = 10000


logic = GameLogic()

best_rateo = 0.0
RATEO = 1.00

IMPROVEMENTS = 0
IMPROVEMENTS_MAX = 7


def start_game():
    global best_rateo, RATEO, IMPROVEMENTS, IMPROVEMENTS_MAX

    games = 0

    board = Board()
    game_logic = GameLogic()
    
    # create players
    player1 = Player(0,"bot00",PlayerStats())
    player2 = Player(1,"bot01",PlayerStats())
    board.spawnPlayers(player1,player2)
        
    DECK_SIZE = 20
    INITIAL_CARDS_GIVEN = 5

    
    while games < MAX_SIMULATED_GAMES:
        
        
        # reset scores
        board.Player1.localGameTurnWins = 0
        board.Player2.localGameTurnWins = 0

        # setup players without resetting their data (stats)
        board.Player1.cards = []
        board.Player2.cards = []
        
        board.Player1.deck = []
        board.Player2.deck = []
        
        
        # give cards to each player
        for i in range(0,2):
            for q in range(0,DECK_SIZE):

                TOTAL_COINFLIPS = random.randint(0,3) 
                REQUIRED_HEADS = random.randint(0,TOTAL_COINFLIPS)
                move = Move(
                    logic=f"""
                    IF HEADS >= {REQUIRED_HEADS} THEN ATTACK*HEADS
                    """,
                    move_type="Attack",
                    energy_cost=random.randint(0,4),
                    damage=random.choice([20,25,30,35,45,50,55,60,70,80,90]),

                    coinflips=TOTAL_COINFLIPS,
                )
                moves = [move]
                card = PokemonCard(q,False,0,random.choice([100,120,140,160,180,110,130,150,170,190,200,210,220,230,240]),moves)
                
                if i == 0:
                    board.Player1.deck.append(card)
                else:
                    board.Player2.deck.append(card)
        
        # shuffle deck
        board.Player1.shuffleDeck()
        board.Player2.shuffleDeck()

        # give initial cards
        board.Player1.drawCard(INITIAL_CARDS_GIVEN)
        board.Player2.drawCard(INITIAL_CARDS_GIVEN)
        
        # who begins, track it
        board.PlayerTurn = random.randint(0,1)
        starting_player:int = board.PlayerTurn

        if board.PlayerTurn == 1:
            board.Player2.stats.total_games_first += 1
        else:
            board.Player1.stats.total_games_first += 1
        
        # reset board
        board.TotalTurns = 0

        #print("Initial cards: ",len(board.Player1.cards))
        #print("Initial cards: ",len(board.Player2.cards))

        gameFinished = False
        while not gameFinished:
            
            # assign player turn
            if board.PlayerTurn == 1:
                player = board.Player2
                opponent = board.Player1
            else:
                player = board.Player1
                opponent = board.Player2
            
            # contition stop
            if player.stats.gold_wins >= 1000:
                games = MAX_SIMULATED_GAMES
                break

            # stats
            player.stats.total_turns += 1

            # give energy
            if board.TotalTurns >= 1:
                player.energy = 1
                player.drawCard(1)

            # check if top card needs to be placed on board slot 0 (main pokemon)
            if player.Terrain[0] == None:
                # place card logic here
                player.placeCard()
            
            # check if we have used our free energy
            # try attacking once card has been placed, given the turn id is greater than 0 (can not attack on the first turn) + can not attack empty slots
            if board.TotalTurns > 0 and player.Terrain[0] is not None and opponent.Terrain[0] is not None:
                #print("attack")
                card1 = player.Terrain[0]
                card2 = opponent.Terrain[0]
                
                # local player is always the attacker
                # pick a random move from the card
                move = random.choice(card1.moves)

                # apply buffs,debuffs on the move
                game_logic.flip_coin(move.coinflips)
                move = move.execute_logic(game_logic)

                # stats
                player.stats.total_coin_tosses += move.coinflips
                player.stats.total_coin_tosses_wins += game_logic.variables["HEADS"]
                
                card2 = card2.applyDamage(move._TotalDamage)
                #print("hp",card2.hp, move.damage, move._TotalDamage)

                # Update stats
                player.stats.total_damage_inflicted += move._TotalDamage
                opponent.stats.total_damage_received += move._TotalDamage

                if card2.hp <= 0:
                    
                    # stats
                    player.stats.total_monsters_killed += 1
                    opponent.stats.total_monsters_lost += 1

                    if card2.isEx:
                        player.localGameTurnWins += 1

                        player.stats.total_ex_killed += 1
                        opponent.stats.total_ex_lost += 1
                        

                    # card got killed, remove it from terrain and put another one
                    opponent.Terrain[0] = None #tmp hack for testing, need to detect proper card slot

                    # also increase score by 1 to localplayer
                    player.localGameTurnWins += 1

                    # check if current player has won the game
                    if player.localGameTurnWins >= 3:
                        player.stats.wins += 1
                        
                        
                        # game win stats
                        if opponent.localGameTurnWins == 0:
                            player.stats.gold_wins += 1
                        elif opponent.localGameTurnWins == 1:
                            player.stats.silver_wins += 1
                        elif opponent.localGameTurnWins == 2:
                            player.stats.bronze_wins += 1
                        
                        # track how many times initial player has won (see bias)
                        if starting_player == player.id:
                            player.stats.total_games_first_won += 1
                            
                        gameFinished = True
                        break
            
            # check if no cards can be player, (end game)
            if len(player.deck) == 0 or len(opponent.deck) == 0:
                gameFinished = True
                break
            
            if board.TotalTurns >= board.rules.maxTurns:
                gameFinished = True
                break
                

            # at the end of the turn, increase turn by 1
            board.TotalTurns += 1
            board.PlayerTurn = 1 - board.PlayerTurn
        
        games += 1

    # end of simulation, print stats
    for i in range(0,2):
        if i == 0:
            statistics = board.Player1.stats
            name = board.Player1.name
        else:
            statistics = board.Player2.stats
            name = board.Player2.name
            
    

        print(name +" Stats:")

        print(" ","Wins: ",statistics.wins)
        print(" ","Games started as first player: ",statistics.total_games_first)
        print(" ","total_damage_inflicted: ",statistics.total_damage_inflicted)
        print(" ","total_damage_received: ",statistics.total_damage_received)
        print(" ","total_coin_tosses: ",statistics.total_coin_tosses)
        print(" ","total_coin_tosses_wins: ",statistics.total_coin_tosses_wins)
        print(" ","gold_wins: ",statistics.gold_wins)
        print(" ","silver_wins: ",statistics.silver_wins)
        print(" ","bronze_wins: ",statistics.bronze_wins)
        print(" ","total_monsters_killed: ",statistics.total_monsters_killed)
        print(" ","total_monsters_lost: ",statistics.total_monsters_lost)
        print(" ","total_turns: ",statistics.total_turns)

        print("Ties: ", MAX_SIMULATED_GAMES - board.Player2.stats.wins - board.Player1.stats.wins)



start_game()
