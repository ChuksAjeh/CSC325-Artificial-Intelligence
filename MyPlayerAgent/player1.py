import numpy as np
import copy
from misc import legalMove
from misc import winningTest
from gomokuAgent import GomokuAgent

class Player(GomokuAgent):
    # def __init__(self, ID, BOARD_SIZE, X_IN_A_LINE):
    #     super(Player, self).__init__(ID,BOARD_SIZE, X_IN_A_LINE)

    def minmax(self, board):
        """Given a state in a game, calculate the best move by searching
        forward all the way to the terminal states. [Figure 5.3]"""
        # return which player it is to move in this state. ** We may need to change the
        player_check = True  # true if us false if the other player.
        player = self.to_move(player_check)

        def max_value(board):
            if self.terminal_test(board):
                return self.utility(board, player)
            v = -np.inf
            move = [0,0]
            x = v

            for a in self.actions(board):
                v = max(v, min_value(self.result(board, a)))
                if v != x:
                    move = a
            return move

        def min_value(board):
            if self.terminal_test(board):
                return self.utility(board, player)
            v = np.inf
            for a in self.actions(board):
                v = min(v, max_value(self.result(board, a)))
            return v
        # Body of minmax_decision:
        return max(self.actions(board), key=lambda a: min_value(self.result(board, a)))

    def utility(self, board, player):
        raise NotImplementedError

    def actions(self, board):
        actions = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board2 = copy.copy(board)
                    board2[i][j] = self.ID
                    actions.append([i, j])
        print(actions)
        return actions

    def move(self, board):
        # while True:
        #     moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
        #     if legalMove(board, moveLoc):
        #         return moveLoc
        return self.minmax(board)
    """Return the state that results from making a move from a state."""

    def result(self, board, action):
        # return the location of where we want to place our counter.
        ##place the new counter on the board.
        board[action] = self.ID

        # get a score of the board
        boardPrime = np.rot90(board)
        sum = 0
        sum += self.diagCount(self.ID, board, self.X_IN_A_LINE)
        sum += self.rowCount(self.ID, board, self.X_IN_A_LINE)
        sum += self.diagCount(self.ID, boardPrime, self.X_IN_A_LINE)
        sum += self.rowCount(self.ID, boardPrime, self.X_IN_A_LINE)
        return sum

    # return whose turn it is to move.
    # if it is our turn -> player_check is true then return our ID.
    # Otherwise it is not our turn it is the enemy's turn and we need to
    # figure out the id.
    def to_move(self, player_check):
        if player_check:
            return self.ID
        else:
            if self.ID == 1:
                return -1
            else:
                return 1

    # return a boolean as to whether we have won or not
    def terminal_test(self, board):
        return winningTest(self.ID, board, self.X_IN_A_LINE)

    def rowCount(self, playerID, board, X_IN_A_LINE):
        BOARD_SIZE = board.shape[0]
        sum = 0
        for r in range(BOARD_SIZE - X_IN_A_LINE):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                i = 0
                while board[r, c + i] == playerID:
                    if i == 0:
                        i += 1
                    elif i == 1:
                        i += 1
                        sum += 2
                    else:
                        i += 1
                        sum += 1
        return sum

    def diagCount(self, playerID, board, X_IN_A_LINE):
        BOARD_SIZE = board.shape[0]
        sum = 0
        for r in range(BOARD_SIZE - X_IN_A_LINE):
            for c in range(BOARD_SIZE - X_IN_A_LINE + 1):
                i = 0
                while board[r + i, c + i] == playerID:
                    if i == 0:
                        i += 1
                    elif i == 1:
                        i += 1
                        sum += 2
                    else:
                        i += 1
                        sum += 1
        return sum

