import numpy as np
import time

from misc import legalMove
from misc import winningTest as winTest
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):

    def move(self, board):

        startTime = time.time()
        print("Player", self.ID)

        if self.ID == -1:
            board *= -1

        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                break

        bestMoveLoc = moveLoc
        bestMoveVal = -1000

        moves, counter = self.potentialMoves(board)
        i = 0
        for move in moves:
            #print("index =", index)
            bias = counter[i]
            i += 1
            print("move", move, "bias", bias)
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
        i = 4
        while i > 1 and not moves:

            for move in self.check(board, i, False):
                if move not in moves:
                    moves.append(move)
                    counters.append(i)
            for move in self.check_gap(board, i, False):
                if move not in moves:
                    moves.append(move)
                    counters.append(i)

            for move in self.check(board, i, True):
                if move not in moves:
                    moves.append(move)
                    counters.append(i)
            for move in self.check_gap(board, i, True):
                if move not in moves:
                    moves.append(move)
                    counters.append(i)
            i -= 1


        while not moves:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, moveLoc):
                moves.append(moveLoc)
                counters.append(0)
                break
        set(moves)
        return moves, counters

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

    def row_enders(self, board, X_IN_A_LINE, moves, isCounter, isrotated):
        identity = self.ID
        if isCounter:
            if self.ID == 1:
                identity = -1

        BOARD_SIZE = board.shape[0]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                flag = True
                for i in range(X_IN_A_LINE):
                    if board[r, c + i] != identity:
                        flag = False
                        break
                if flag:
                    if c + X_IN_A_LINE < BOARD_SIZE and board[r, (c + X_IN_A_LINE)] == 0:
                        position = (r, c + X_IN_A_LINE)
                        if position not in moves:
                            moves.append(position)
                    if c - 1 > -1 and board[r, c - 1] == 0:
                        position = (r, c - 1)
                        if position not in moves:
                            moves.append(position)
        return moves

    def diag_enders(self, board, X_IN_A_LINE, moves, isCounter, isrotated):
        identity = self.ID
        if isCounter:
            if self.ID == 1:
                identity = -1

        BOARD_SIZE = board.shape[0]
        for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                flag = True
                for i in range(X_IN_A_LINE):
                    if board[r + i, c + i] != identity:
                        flag = False
                        break
                if flag:
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

    def row_gap(self, board, X_IN_A_LINE, moves, isCounter, isrotated):
        identity = self.ID
        if isCounter:
            if self.ID == 1:
                identity = -1

        position = (-1, -1)
        BOARD_SIZE = board.shape[0]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                count = 0

                for i in range(X_IN_A_LINE):
                    if board[r, c + X_IN_A_LINE -1] == 0 or board[r,c] == 0:
                        break
                    if board[r, c + i] != identity and count < 2:
                        count += 1
                        position = (r, c + i)


                if 2 > count > 0:
                    if board[position] == 0:
                      #  print(moves, " pos ro ", isrotated, position)
                        moves.append(position)
                count = 0
        return moves

    def diag_gap(self, board, X_IN_A_LINE, moves, isCounter, isrotated):
        identity = self.ID
        if isCounter:
            if self.ID == 1:
                identity = -1

        position = (-1, -1)
        BOARD_SIZE = board.shape[0]
        for r in range(BOARD_SIZE - X_IN_A_LINE + 1):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                count = 0
                for i in range(X_IN_A_LINE):
                    if board[r + X_IN_A_LINE - 1, c + X_IN_A_LINE -1] == 0 or board[r, c] == 0:
                        break
                    if board[r + i, c + i] != identity and count < 2:
                        count += 1
                        position = (r + i, c + i)
                if 2 > count > 0:
                    if board[position] == 0:
                       # print(moves, " pos di ", isrotated, position)
                        moves.append(position)

                count = 0
        return moves


    def check(self, board, amount, isCounter):
        board_rot = np.rot90(np.array(board), 3)
        moves = []
        rot_moves = []
        self.diag_enders(board, amount, moves, isCounter,1)
        self.diag_enders(board_rot, amount, rot_moves, isCounter,2)
        self.row_enders(board, amount, moves, isCounter,1)
        self.row_enders(board_rot, amount, rot_moves, isCounter,2)

        for move in rot_moves:
            board_rot_temp = np.array(board_rot)
            board_rot_temp[move] = 5
            board_rot_temp = np.rot90(board_rot_temp)
            np_move = np.where(board_rot_temp == 5)
            true_move = (np_move[0][0], np_move[1][0])
            if true_move not in moves:
                moves.append(true_move)
        return moves

    def check_gap(self, board, amount, isCounter):
        board_rot = np.rot90(np.array(board), 3)
        moves = []
        rot_moves = []

        self.row_gap(board, amount + 1, moves, isCounter,1)
        self.row_gap(board_rot, amount + 1, rot_moves, isCounter,2)
        self.diag_gap(board, amount + 1, moves, isCounter,1)
        self.diag_gap(board_rot, amount + 1, rot_moves, isCounter,2)

        for move in rot_moves:
            board_rot_temp = np.array(board_rot)
            board_rot_temp[move] = 5
            board_rot_temp = np.rot90(board_rot_temp)
            np_move = np.where(board_rot_temp == 5)
            true_move = (np_move[0][0], np_move[1][0])
            if true_move not in moves:
                moves.append(true_move)
               # print("ammened moves", true_move, "bias", amount)
            #print("llll", moves)
        return moves