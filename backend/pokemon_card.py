class PokemonCard:
    def __init__(self, id:int, isEx:bool, stage:int, maxHp:int, moves:dict, energy=0):

        self.id = id

        self.isEx = isEx
        self.stage = stage  # [0,1,2,3]
        
        self.maxHp = maxHp
        self.hp    = self.maxHp
        
        self.type = ""
        self.status_effects = []
        self.moves = moves
        
        self.isBasic = True
        self.energy = energy
        self.weakness = ""

        self.retreatCost = 1
        self.rarity = 0
    
    def applyDamage(self, amount:int):
        self.hp -= amount
        return self
    
    def getValidMoves(self):
        valid_moves = []
        for move in self.moves:
            if self.energy >= move.energy_cost:
                valid_moves.append(move)
        return valid_moves
