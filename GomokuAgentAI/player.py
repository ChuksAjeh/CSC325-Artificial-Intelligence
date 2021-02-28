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


        bestMoveLoc = moveLoc
        bestMoveVal = 999
        for move in self.potentialMoves(board):
            boardPrime = board
            boardPrime[move] = 1
            # Move value here is depth to end state
            moveVal = self.miniMax(boardPrime, 0, False)
            if moveVal < bestMoveVal and moveVal > 0:
                bestMoveLoc = move
                bestMoveVal = moveVal
            elif moveVal == 0 and bestMoveVal == 999:
                bestMoveLoc = move
            print(moveVal)
            break
        return bestMoveLoc

    def potentialMoves(self, board):
        allMoves = []
        boardSize = board.shape[0]
        for i in range(boardSize):
            for j in range(boardSize):
                moveLoc = (i, j)
                if legalMove(board, moveLoc):
                    allMoves.append(moveLoc)
        return allMoves

    def score(self, board, depth):
        if winTest(1, board, self.X_IN_A_LINE):
            return depth
        elif winTest(-1, board, self.X_IN_A_LINE):
            return -depth
        elif not 0 in board:
            return 0

    def isTerminalState(self, board):
        if winTest(1, board, self.X_IN_A_LINE) or winTest(-1, board, self.X_IN_A_LINE) or not 0 in board:
            return True
        return False

    def miniMax(self, board, depth, isMaximising):
        depth += 1

        if self.isTerminalState(board):
            return self.score(board, depth)
        else:
            if isMaximising:
                bestMoveVal = 999
                for move in self.potentialMoves(board):
                    boardPrime = board
                    boardPrime[move] = 1
                    moveVal = self.miniMax(boardPrime, depth, False)
                    if bestMoveVal == 0 and moveVal > 0:
                        bestMoveVal = moveVal
                    elif moveVal > 0 and moveVal < bestMoveVal:
                        bestMoveVal = moveVal
                    elif moveVal == 0 and bestMoveVal == 999:
                        bestMoveVal = moveVal

            else:
                bestMoveVal = -999
                for move in self.potentialMoves(board):
                    boardPrime = board
                    boardPrime[move] = -1
                    moveVal = self.miniMax(boardPrime, depth, True)

                    if bestMoveVal == 0 and moveVal < 0:
                        bestMoveVal = moveVal
                    elif moveVal < 0 and moveVal > bestMoveVal:
                        bestMoveVal = moveVal
                    elif moveVal == 0 and bestMoveVal == -999:
                        bestMoveVal = moveVal

            return bestMoveVal

