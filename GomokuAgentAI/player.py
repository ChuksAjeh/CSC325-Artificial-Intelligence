import numpy as np

from misc import legalMove
from misc import winningTest as winTest
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):



    def move(self, board):
        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                break

        bestMove = moveLoc
        bestMoveVal = -1000
        for move in self.potentialMoves(board):
            boardPrime = board
            boardPrime[move] = 1
            moveVal = self.miniMax(boardPrime, False)
            if moveVal > bestMoveVal:
                bestMove = move
                bestMoveVal = moveVal
        return bestMove

    def potentialMoves(self, board):
        allMoves = []
        boardSize = board.shape[0]
        for i in range(boardSize):
            for j in range(boardSize):
                moveLoc = (i, j)
                if legalMove(board, moveLoc):
                    allMoves.append(moveLoc)
        return allMoves

    def score(self, board):
        if winTest(1, board, self.X_IN_A_LINE):
            return 10
        elif winTest(-1, board, self.X_IN_A_LINE):
            return -10
        elif not 0 in board:
            return 0

    def miniMax(self, board, isMaximising):

        if winTest(1, board, self.X_IN_A_LINE) or winTest(-1, board, self.X_IN_A_LINE) or not (0 in board):
            return self.score(board)
        else:
            moveVal = -1000
            if isMaximising:
                for move in self.potentialMoves(board):
                    boardPrime = board
                    boardPrime[move] = 1
                    moveVal = max(self.miniMax(boardPrime, False), moveVal)
            else:
                for move in self.potentialMoves(board):
                    boardPrime = board
                    boardPrime[move] = -1
                    moveVal = min(self.miniMax(boardPrime, True), moveVal)
            return moveVal

