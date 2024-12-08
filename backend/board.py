from player import *

class Board:
    def __init__(self):
        self.rules = Rules()

        self.PlayerTurn = 0
        self.TotalTurns = 0

        self.Player1 = None
        self.Player2 = None
    
    def spawnPlayers(self, Player1:Player, Player2:Player):
        self.Player1 = Player1
        self.Player2 = Player2

class Rules:
    def __init__(self):
        self.disabledSlots = [] #0, 1, 2, 3
        self.disabledCardIds = []
        self.disabledCardTypes = []
        self.disabledCardStats = []
        self.isDrawingDisabled = False
        self.isEnergyDisabled = False
        self.isItemDisabled = False
        self.maxTurns = 30
