import numpy as np
import time

from misc import legalMove
from misc import winningTest as winTest
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):

    def move(self, board):

        startTime = time.time()

        if self.ID == -1:
            board *= -1

        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                break

        bestMoveLoc = moveLoc
        bestMoveVal = -1000

        moves, bias = self.potentialMoves(board)
        for move in moves:
            boardPrime = np.array(board)

            boardPrime[move] = 1
            moveVal = self.miniMax(boardPrime, 3, -10000, 10000, False)

            if bias != 0:
                if bias == 4:
                    moveVal += 200
                if bias == 3:
                    moveVal += 40
                if bias == 2:
                    moveVal += 20


            if moveVal > bestMoveVal:
                bestMoveVal = moveVal
                bestMoveLoc = move

        executionTime = (time.time() - startTime)
        print('Execution time in seconds:' + str(executionTime))

        print(bestMoveLoc)
        return bestMoveLoc

    def potentialMoves(self, board):
        moves = []
        counters = []
        double_counters = []
        boardSize = board.shape[0]
        bias = 0

        for move in self.check(board, 4, False):
            if move not in moves:
                moves.append(move)

        i = 5
        while i > 1 and not moves:
            for move in self.check(board, i, True):
                if move not in moves:
                    moves.append(move)

                # if move in counters and move not in double_counters:
                #     double_counters.append(move)
                # elif move not in counters:
                #     counters.append(move)

            i -= 1

        i = 3
        while i > 0 and not moves:
            for move in self.check(board, i, False):
                if move not in moves:
                    moves.append(move)
            i -= 1

        while not moves:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                moves.append(moveLoc)
                break
        set(moves)

        return moves, bias

    def score(self, board):
        def rowCount(playerID, board, X_IN_A_LINE):
            BOARD_SIZE = board.shape[0]
            total_in_line = 0
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                    cur_run_count = 0
                    for i in range(X_IN_A_LINE):
                        if board[r, c + i] == playerID:
                            cur_run_count += 1
                            if cur_run_count == 2:
                                total_in_line += 2
                            elif cur_run_count > 2:
                                total_in_line += 1
                        else:
                            break
            return total_in_line

        def diagCount(playerID, board, X_IN_A_LINE):
            BOARD_SIZE = board.shape[0]
            total_in_line = 0
            for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
                for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                    cur_run_count = 0
                    for i in range(X_IN_A_LINE):
                        if board[r + i, c + i] == playerID:
                            cur_run_count += 1
                            if cur_run_count == 2:
                                total_in_line += 2
                            elif cur_run_count > 2:
                                total_in_line += 1
                        else:
                            break
            return total_in_line

        def diagPlusRowCount(playerID, board, X_IN_A_LINE):
            return diagCount(playerID, board, X_IN_A_LINE) + rowCount(playerID, board, X_IN_A_LINE)

        boardPrime = np.array(board)
        boardPrimeRot = np.rot90(np.array(boardPrime))

        player_score = diagPlusRowCount(1, boardPrime, self.X_IN_A_LINE) + \
                       diagPlusRowCount(1, boardPrimeRot, self.X_IN_A_LINE)

        opp_score = diagPlusRowCount(-1, boardPrime, self.X_IN_A_LINE) + \
                    diagPlusRowCount(-1, boardPrimeRot, self.X_IN_A_LINE)

        if winTest(1, boardPrime, self.X_IN_A_LINE):
            return 100
        elif winTest(-1, boardPrime, self.X_IN_A_LINE):
            return -100
        elif not 0 in board:
            return 0

        return player_score - opp_score

    def isTerminalState(self, board):
        if winTest(1, board, self.X_IN_A_LINE) or winTest(-1, board, self.X_IN_A_LINE) or not 0 in board:
            return True
        return False

    def miniMax(self, board, depth, alpha, beta, isMaximising):


        if self.isTerminalState(board) or depth == 0:
            return self.score(board)
        else:
            if isMaximising:
                moveVal = -1000
                moves, bias = self.potentialMoves(board)
                for move in moves:
                    boardPrime = np.array(board)
                    boardPrime[move] = 1
                    newMoveVal = self.miniMax(boardPrime, depth - 1, alpha, beta, False)
                    if bias != 0:
                        if bias == 4:
                            newMoveVal += 60
                        if bias == 3:
                            newMoveVal += 40
                        if bias == 2:
                            newMoveVal += 20

                    moveVal = max(newMoveVal, moveVal)
                    alpha = max(alpha, moveVal)
                    if beta <= alpha:
                        break
                return moveVal
            else:
                moveVal = 1000
                moves, bias = self.potentialMoves(board)
                for move in moves:
                    boardPrime = np.array(board)
                    boardPrime[move] = -1
                    newMoveVal = self.miniMax(boardPrime, depth - 1, alpha, beta, True)
                    if bias != 0:
                        if bias == 4:
                            newMoveVal -= 60
                        if bias == 3:
                            newMoveVal -= 40
                        if bias == 2:
                            newMoveVal -= 20

                    moveVal = min(newMoveVal, moveVal)
                    beta = min(alpha, moveVal)
                    if beta <= alpha:
                        break
                return moveVal

    def row_enders(self, board, X_IN_A_LINE, moves, isCounter):
        identity = self.ID
        if isCounter:
            identity = -1

        BOARD_SIZE = board.shape[0]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                flag = True
                for i in range(X_IN_A_LINE):
                    if board[r, c + i] != identity:
                        if c + i + 1 < BOARD_SIZE:
                            if board[r, c] == identity:
                                if board[r, c + i + 1] == identity and board[r, c + i] == 0:
                                    position = (r, c + i)
                                    moves.append(position)
                        flag = False
                        break
                if flag:
                    if c + X_IN_A_LINE + 1 < BOARD_SIZE and board[r, (c + X_IN_A_LINE)] == identity \
                            and board[r, (c + X_IN_A_LINE) + 1] == 0:
                        position = (r, c + X_IN_A_LINE + 1)
                        if position not in moves:
                            moves.append(position)
                    if c + X_IN_A_LINE < BOARD_SIZE and board[r, (c + X_IN_A_LINE)] == 0:
                        position = (r, c + X_IN_A_LINE)
                        if position not in moves:
                            moves.append(position)
                    if c - 1 > -1 and board[r, c - 1] == 0:
                        position = (r, c - 1)
                        if position not in moves:
                            moves.append(position)
        return moves

    def diag_enders(self, board, X_IN_A_LINE, moves, isCounter):
        identity = self.ID
        if isCounter:
            identity = -1

        BOARD_SIZE = board.shape[0]
        for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                flag = True
                for i in range(X_IN_A_LINE):
                    if board[r + i, c + i] != identity:
                        if r + i + 1 < BOARD_SIZE and c + i + 1 < BOARD_SIZE:
                            if board[r, c] == identity:
                                if board[r + i + 1, c + i + 1] == identity and board[r + i, c + i] == 0:
                                    position = (r + i, c + i)
                                    moves.append(position)
                        flag = False
                        break
                if flag:
                    if c + X_IN_A_LINE + 1 < BOARD_SIZE and r + X_IN_A_LINE + 1 < BOARD_SIZE \
                            and board[(r + X_IN_A_LINE), (c + X_IN_A_LINE)] == identity \
                            and board[(r + X_IN_A_LINE) + 1, (c + X_IN_A_LINE) + 1] == 0:
                        position = (r + X_IN_A_LINE + 1, c + X_IN_A_LINE + 1)
                        if position not in moves:
                            moves.append(position)

                    if c + X_IN_A_LINE < BOARD_SIZE and r + X_IN_A_LINE < BOARD_SIZE \
                            and board[(r + X_IN_A_LINE), (c + X_IN_A_LINE)] == 0:
                        position = (r + X_IN_A_LINE, c + X_IN_A_LINE)
                        if position not in moves:
                            moves.append(position)

                    if c - 1 > -1 and r - 1 > -1 and board[r - 1, c - 1] == 0:
                        position = (r - 1, c - 1)
                        if position not in moves:
                            moves.append(position)
        return moves

    def check(self, board, amount, isCounter):
        board_rot = np.rot90(np.array(board))
        moves = []
        rot_moves = []

        self.diag_enders(board, amount, moves, isCounter)
        self.diag_enders(board_rot, amount, rot_moves, isCounter)
        self.row_enders(board, amount, moves, isCounter)
        self.row_enders(board_rot, amount, rot_moves, isCounter)

        for move in rot_moves:
            board_rot_temp = np.array(board_rot)
            board_rot_temp[move] = 5
            board_rot_temp = np.rot90(board_rot_temp, 3)
            np_move = np.where(board_rot_temp == 5)
            true_move = (np_move[0][0], np_move[1][0])
            if true_move not in moves:
                moves.append(true_move)
        return moves
