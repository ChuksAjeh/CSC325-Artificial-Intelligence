import numpy as np
import copy
from misc import legalMove
from misc import winningTest as winTest
from gomokuAgent import GomokuAgent

class Player(GomokuAgent):

    def move(self, board):
        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                break

        checked_move = check(self, board, 3)
        if checked_move != [-1,-1]:
            print("move =", checked_move)
            return tuple(checked_move)

        checked_move = check(self, board, 2)
        if checked_move != [-1,-1]:
            print("move =", checked_move)
            return tuple(checked_move)

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

def counter_row(playerID, board, X_IN_A_LINE):
    BOARD_SIZE = board.shape[0]
    position = [50, 50]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
            flag = True
            for i in range(X_IN_A_LINE):
                if board[r, c + i] != playerID:
                    flag = False
                    break
            if flag:
                if c + X_IN_A_LINE + 1 < BOARD_SIZE and board[r, (c + X_IN_A_LINE)] == playerID \
                        and board[r, (c + X_IN_A_LINE) + 1] == 0:
                    print("move found1", [r, c + X_IN_A_LINE + 1])
                    position = [r, c + X_IN_A_LINE + 1]
                    return position
                if c + X_IN_A_LINE + 1 < BOARD_SIZE and board[r, (c + X_IN_A_LINE)] == 0:
                    print("move found2", [r, c + X_IN_A_LINE])
                    position = [r, c + X_IN_A_LINE]
                    return position
                if c - 1 > -1 and board[r, c - 1] == 0:
                    print("move found3", [r, c - 1])
                    position = [r, c - 1]
                    return position

    return position

def counter_diag(playerID, board, X_IN_A_LINE):
    BOARD_SIZE = board.shape[0]
    position = [50, 50]
    for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
        for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
            flag = True
            for i in range(X_IN_A_LINE):
                if board[r + i, c + i] != playerID:
                    flag = False
                    break
            if flag:
                if c + X_IN_A_LINE + 1 < BOARD_SIZE and r + X_IN_A_LINE + 1 < BOARD_SIZE \
                        and board[(r + X_IN_A_LINE), (c + X_IN_A_LINE)] == playerID \
                        and board[(r + X_IN_A_LINE) + 1, (c + X_IN_A_LINE) + 1] == 0:
                    print("moves found4", [r + X_IN_A_LINE + 1, c + X_IN_A_LINE + 1])
                    position = [r + X_IN_A_LINE + 1, c + X_IN_A_LINE + 1]
                    return position

                if c + X_IN_A_LINE < BOARD_SIZE and r + X_IN_A_LINE < BOARD_SIZE \
                        and board[(r + X_IN_A_LINE), (c + X_IN_A_LINE)] == 0:
                    print("moves found5", [r + X_IN_A_LINE, c + X_IN_A_LINE])
                    position = [r + X_IN_A_LINE, c + X_IN_A_LINE]
                    return position

                if c - 1 > -1 and r - 1 > -1 and board[r - 1, c - 1] == 0:
                    print("moves found6", [r - 1, c - 1])
                    position = [r - 1, c - 1]
                    return position

    return position

def check(self, board, i):
    board_rot = copy.copy(board)
    board_rot = np.rot90(board_rot, 3)
    identity = 1
    amount = i
    position = [-1, -1]

    if self.ID == 1:
        identity = -1

    move = counter_diag(identity, board, amount)
    if move != [50, 50]:
        return move

    move = counter_diag(identity, board_rot, amount)
    if move != [50, 50]:
        board_rot[tuple(move)] = 5
        board_rot = np.rot90(board_rot)
        move = list(np.where(board_rot == 5))
        return move

    move = counter_row(identity, board, amount)
    if move != [50, 50]:
        return move

    move = counter_row(identity, board_rot, amount)
    if move != [50, 50]:
        board_rot[tuple(move)] = 5
        board_rot = np.rot90(board_rot)
        move = np.where(board_rot == 5)
        return move

    return position