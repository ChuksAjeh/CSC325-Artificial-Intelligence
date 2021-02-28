import numpy as np

from misc import legalMove
from misc import winningTest as winTest
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):

    def move(self, board):
        temp_board = np.array(board)
        # print("Starting board ",board)
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

        print("PLAYER: ", self.ID, " bestMove", bestMove)
        # print("ending board", board)
        self.successors(bestMove, temp_board)
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

    # return a list of succesors
    # {
    #     {0,0,0},
    #     {0,1,0},
    #     {0,0,0},
    # }
    def successors(self, bestMove, board):
        successors = []
        i = bestMove[0]
        j = bestMove[1]
        # right
        if 0 < i + 1 <= self.BOARD_SIZE and 0 < j <= self.BOARD_SIZE:
            successors.append(("right", board[i + 1, j]))  # DONE
        else:
            successors.append(("right", 99))
        # left
        if 0 < (i - 1) <= self.BOARD_SIZE and 0 < j <= self.BOARD_SIZE:
            successors.append(("left", board[i - 1, j], (i - 1, j)))  # DONE
        else:
            successors.append(("left", 99))
        # # up
        if 0 < i <= self.BOARD_SIZE and 0 < (j + 1) <= self.BOARD_SIZE:
            successors.append(("DOWN", board[i, j + 1]))  # DONE
        else:
            successors.append(("down ", 99))
        # # Up left
        if 0 < (i - 1) <= self.BOARD_SIZE and 0 < (j + 1) <= self.BOARD_SIZE:
            successors.append(("DOWN left", board[i - 1, j + 1]))  # DONE
        else:
            successors.append(("down left", 99))
        # # up right:

        if 0 < (i + 1) <= self.BOARD_SIZE and 0 < (j + 1) <= self.BOARD_SIZE:
            successors.append(("DOWN right", board[i + 1, j + 1]))  # DONE
        else:
            successors.append(("down right", 99))
        # # down
        if 0 < i <= self.BOARD_SIZE and 0 < (j - 1) <= self.BOARD_SIZE:
            successors.append(("UP", board[i, j - 1], (i, j - 1)))  # DONE
        else:
            successors.append(("up", 99))
        # # down left:
        if 0 < (i - 1) <= self.BOARD_SIZE and 0 < (j - 1) <= self.BOARD_SIZE:
            successors.append(("UP left", board[i - 1, j - 1]))  # DONE
        else:
            successors.append(("up left", 99))
        # # down right:
        if 0 < (i + 1) <= self.BOARD_SIZE and 0 < (j - 1) <= self.BOARD_SIZE:
            successors.append(("UP right", board[i + 1, j - 1]))  # DONE
        else:
            successors.append(("up right", 99))


        print("PLAYER: ", self.ID, " ", successors)

    def get_color(self,i):
        return "\033[3{}m{}\033[0m".format(i+1, i)

