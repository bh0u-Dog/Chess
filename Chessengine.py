# This class is responsible for stroing all the information about the current state of chess game.

class GameState():
    def __init__(self):
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR'],
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.knightMoves = [[2,-1],[2,1],[-2,-1],[-2,1],[-1,2],[1,2],[-1,-2],[1,-2]]
        self.whitepawnMoves = [[0,-1],[0,-2]]
        self.blackpawnMoves = [[0,1],[0,2]]
        self.rookMoves = []
        self.kingMoves = [[1,0],[-1,0],[-1,1],[0,1],[0,-1],[1,1],[1,-1],[-1,-1]]
        self.bishopMoves = []
        self.queenMoves = []

        # Docs - i am having empty lists because of some reason even i dont know but it still works so jokes on you. Jk i just used them because they work. FINE