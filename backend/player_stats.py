class PlayerStats:
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.knockout_without_backup = 0
        self.deckouts = 0
        
        self.total_games = 0
        self.total_games_first = 0
        self.total_games_first_won = 0
        self.total_turns = 0
        
        self.gold_wins = 0
        self.silver_wins = 0
        self.bronze_wins = 0

        self.total_damage_inflicted = 0
        self.total_damage_received = 0
        self.total_healing_done = 0
        self.total_coin_tosses = 0
        self.total_coin_tosses_wins = 0

        self.total_monsters_placed = 0
        self.total_monsters_lost = 0
        self.total_monsters_killed = 0

        self.total_ex_killed = 0
        self.total_ex_lost = 0

        self.total_energy_placed = 0
        self.total_items_used = 0

        self.games_turns = []