class Move:
    def __init__(self, logic, move_type, energy_cost=1, damage=0, coinflips=0, debuffs=[]):
        self.logic = logic
        self.move_type = move_type
        
        self.damage = damage
        self.coinflips = coinflips
        self.debuffs = debuffs
        self.cards_drawn = 0
        self.energy_cost = energy_cost

        # do not edit
        self._TotalDamage = 0
        self._TotalHealing = 0


    def execute_logic(self, game_logic):
        move_data = game_logic.parse_logic(self)
        return move_data