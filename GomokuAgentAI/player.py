"""
    CSC_325 CW 1 Submission
    player.py class containing code for an AI agent to play NxN gomoku against an opponent
    Authors:
    Chukwuka Ajeh - 991129
    Leon Mills - 979610
    Jack Goudie - 985964

    Overall comments
    During development we started with minimax as a base, before adapting the code to use Alpha-beta
    pruning. The minimax performed well but was too slow in winning games. Alpha-beta had a much better performance
    winning games faster. To make sure our AI was making better decisions we used a number of strategies based upon
    the idea 'if we can't win then we go for a draw'. This was reflected in our counter strategies. Making sure to
    counter pieces should the have two, three or four in a row or in a broken line. To make sure our code was optimal
    we ran it against a prior version that used minimax which it handily beat consistently as well as then running it
    against itself which would cause the game to result in a draw repeatedly .
"""

import time

import numpy as np

from gomokuAgent import GomokuAgent
from misc import legalMove
from misc import winningTest as winTest


class Player(GomokuAgent):
    """
    Decides the move for our agent to make when called by the game class

    Uses potentialMoves function to produce a list of moves to feed into minimax, with the move producing the best score
    output being the chosen move

    Makes use of biases to ensure that counter and attacking moves are given additional precedence

    Returns a move location in the form of (row, column)
    """

    def move(self, board):
        startTime = time.time()

        # This snippet flips the board if we are player -1, meaning the code can run as if we were player 1
        # Could possibly be fixed with better generalisation of later code
        if self.ID == -1:
            board *= -1

        best_move_loc = None
        best_move_val = -1000

        for move_and_bias in self.potentialMoves(board):
            # Making sure that we are not likely to go over the time limit by exploring any more moves
            if (time.time() - startTime) > 3.5:
                break

            move = move_and_bias[0]
            bias = move_and_bias[1]

            board_prime = np.array(board)
            board_prime[move] = 1

            # Initial minimax call with board after potential move has been made, setting the maximum depth for search
            # to 4, setting alpha to large negative and beta to large positive, maximising player set to False
            move_val = self.miniMax(board_prime, 4, -10000, 10000, False)

            if bias != 0:
                if bias == 4:
                    move_val += 60
                if bias == 3:
                    move_val += 40
                if bias == 2:
                    move_val += 20

            if move_val > best_move_val:
                best_move_val = move_val
                best_move_loc = move

        # executionTime = (time.time() - startTime)
        # print('Execution time in seconds:' + str(executionTime))

        return best_move_loc

    """
    Returns a list of positions of potential moves on the board passed to it

    Ordering of move finding is important for effective counters or attacks

    Firstly checks for moves that will advance our lines
    Then checks for moves that will counter opponents lines
    i here is the length of lines being looked for (4 looks for patterns that given an extra piece would be 5)

    If there are no counters and no attacking moves then we look for a random location on the board until we find
    an empty space to play into
    """

    def potentialMoves(self, board):
        moves = []
        i = 4
        while i > 1 and not moves:

            for move in self.lineCheck(board, i, False):
                if move not in moves:
                    moves.append([move, i])

            for move in self.lineCheck(board, i, True):
                if move not in moves:
                    moves.append([move, i])
            i -= 1

        while not moves:
            move_loc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            if legalMove(board, move_loc):
                moves.append([move_loc, 0])
                break

        return moves

    """
    Determines the score of the current player for the given board, this score is used by the minimax for comparisons

    Score is worked out by finding the total number of pieces that are part of a run/line for each player and taking
    the opponents score away from the agent score

    If the board is in a winning state for either player it will return a score of 100 if agent wins, -100 if opponent
    wins and 0 if the game is a draw
    """

    def score(self, board):

        # Counts the number of pieces that are part of any horizontal run of pieces
        def rowSum(playerID, board, win_length):
            board_size = board.shape[0]
            total_in_line = 0
            for r in range(board_size):
                for c in range(board_size - win_length + 1):
                    cur_run_count = 0
                    for i in range(win_length):
                        if board[r, c + i] == playerID:

                            # first piece will not affect total count as it could just be a lone piece
                            cur_run_count += 1
                            if cur_run_count == 2:
                                # second piece in a row confirms that first piece is in a row so 2 is added to total
                                total_in_line += 2
                            elif cur_run_count > 2:
                                # anything greater than 2 only adds one to total
                                total_in_line += 1
                        else:
                            break
            return total_in_line

        # Counts the number of pieces that are part of any diagonal run of pieces
        def diagSum(playerID, board, win_length):
            board_size = board.shape[0]
            total_in_line = 0
            for r in range(board_size - win_length + 1):
                for c in range(board_size - win_length + 1):
                    cur_run_count = 0
                    for i in range(win_length):
                        if board[r + i, c + i] == playerID:
                            cur_run_count += 1
                            if cur_run_count == 2:
                                total_in_line += 2
                            elif cur_run_count > 2:
                                total_in_line += 1
                        else:
                            break
            return total_in_line

        # Sum of the diag and row counts
        def rowDiagSum(playerID, board, win_length):
            return diagSum(playerID, board, win_length) + rowSum(playerID, board, win_length)

        board_prime = np.array(board)
        boardPrimeRot = np.rot90(np.array(board_prime))

        # Checking win conditions
        if winTest(1, board_prime, self.X_IN_A_LINE):
            return 100
        elif winTest(-1, board_prime, self.X_IN_A_LINE):
            return -100
        elif 0 not in board:
            return 0

        player_score = rowDiagSum(1, board_prime, self.X_IN_A_LINE) + rowDiagSum(1, boardPrimeRot, self.X_IN_A_LINE)
        opp_score = rowDiagSum(-1, board_prime, self.X_IN_A_LINE) + rowDiagSum(-1, boardPrimeRot, self.X_IN_A_LINE)

        return player_score - opp_score

    # Boolean function to check if a given board is in a terminal state, ie either player has won or it is a draw
    def isTerminalState(self, board):
        if winTest(1, board, self.X_IN_A_LINE) or winTest(-1, board, self.X_IN_A_LINE) or 0 not in board:
            return True
        return False

    """
    Minimax function, iteratively searches through moves until reaching a given depth or a terminal state. The board
    is cloned and then altered as it is passed through the tree so successive moves can be inspected

    Move values are calculated using score function at bottom of search tree

    Maximising player searches for maximum score while minimising player is looking for lowest score

    Bias values are used to add weight to moves which are counters or attacking moves, with a greater bias given to
    moves which create or obstruct longer rows

    Alpha beta pruning is in place to lessen the search space, leaves are pruned from the tree if it is known that the
    result will not affect the outcome of the search

    Potential moves are generated by the potentialMoves function, whose search trees are then explored to produce an
    overall score for that move.

    A set of moves is chosen at depth zero and then each is passed into minimax, the move that produces the best score
    is the move that the agent chooses as the optimal move
    """

    def miniMax(self, board, depth, alpha, beta, isMaximising):
        if self.isTerminalState(board) or depth == 0:
            return self.score(board)
        else:
            if isMaximising:
                move_val = -1000
                for move_and_bias in self.potentialMoves(board):
                    move = move_and_bias[0]
                    bias = move_and_bias[1]

                    board_prime = np.array(board)
                    board_prime[move] = 1

                    # Recursive minimax call, setting maximising player to False
                    new_move_val = self.miniMax(board_prime, depth - 1, alpha, beta, False)

                    if bias != 0:
                        if bias == 4:
                            new_move_val += 60
                        if bias == 3:
                            new_move_val += 40
                        if bias == 2:
                            new_move_val += 20

                    move_val = max(new_move_val, move_val)
                    alpha = max(alpha, move_val)
                    if beta <= alpha:
                        break
                return move_val
            else:
                move_val = 1000
                for move_and_bias in self.potentialMoves(board):
                    move = move_and_bias[0]
                    bias = move_and_bias[1]

                    board_prime = np.array(board)
                    board_prime[move] = -1

                    # Recursive minimax call, setting maximising player to True
                    new_move_val = self.miniMax(board_prime, depth - 1, alpha, beta, True)

                    if bias != 0:
                        if bias == 4:
                            new_move_val -= 60
                        elif bias == 3:
                            new_move_val -= 40
                        elif bias == 2:
                            new_move_val -= 20

                    move_val = min(new_move_val, move_val)
                    beta = min(alpha, move_val)
                    if beta <= alpha:
                        break
                return move_val

    """
        Row enders produces all positions at the end and beginning of a running length of values in a row (Either a run of
        1s or a run of -1s). It loops through all acceptable positions on the board checking all positions (up to the run
        length) to the right from that position.

        run_length refers to the length of values we are checking each loop.

        is_counter is a boolean to identify whether or not we are checking connected values of the opposing player or ours.
        If is_counter is true then the method will search for connections of the opposing identity, it will search ours if
        false.

        Moves is the list of moves

        board is the current state of the game board.
        """

    def row_enders(self, board, run_length, moves, is_counter):
        identity = self.ID
        if is_counter:
            if self.ID == 1:
                identity = -1

        board_size = board.shape[0]
        for r in range(board_size):
            for c in range(board_size - run_length + 1):
                flag = True
                for i in range(run_length):
                    # will break out of the loop if the number of successive values doesn't match the run length.
                    if board[r, c + i] != identity:
                        flag = False
                        break
                if flag:
                    # Adds the right most end that is 0
                    if c + run_length < board_size and board[r, (c + run_length)] == 0:
                        position = (r, c + run_length)
                        if position not in moves:
                            moves.append(position)
                    # Adds the left most end that is 0
                    if c > 0:
                        if board[r, c - 1] == 0:
                            position = (r, c - 1)
                            if position not in moves:
                                moves.append(position)
        return moves

    """
    Diag enders produces all positions at the end and beginning of a running length of values in succession 
    diagonally (Either a run of 1s or a run of -1s). It loops through all acceptable positions on the board checking 
    all positions (up to the run length) diagonally from that position. 

    run_length refers to the length of values we are checking each loop.

    is_counter is a boolean to identify whether or not we are checking connected values of the opposing player or ours.
    If is_counter is true then the method will search for connections of the opposing identity, it will search ours if 
    false.

    Moves is the list of moves

    board is the current state of the game board.
    """

    def diag_enders(self, board, run_length, moves, is_counter):
        identity = self.ID
        if is_counter:
            if self.ID == 1:
                identity = -1

        board_size = board.shape[0]
        for r in range(board_size - run_length + 1):
            for c in range(board_size - run_length + 1):
                flag = True
                for i in range(run_length):
                    # will break out of the loop if the number of successive values doesn't match the run length.
                    if board[r + i, c + i] != identity:
                        flag = False
                        break
                if flag:
                    # Adds the right most end that is 0
                    if c + run_length < board_size and r + run_length < board_size \
                            and board[r + run_length, c + run_length] == 0:
                        position = (r + run_length, c + run_length)
                        if position not in moves:
                            moves.append(position)
                    # Adds the left most end that is 0
                    if c > 0 and r > 0:
                        if board[r - 1, c - 1] == 0:
                            position = (r - 1, c - 1)
                            if position not in moves:
                                moves.append(position)
        return moves

    """
    Row Gap produces all positions that a gap is formed in a run of values found in a row (Either a run of 1s or -1s).
    It loops through all the acceptable positions on the board checking all positions (up to the run length) to the 
    right from that position. If in the run of values there is exactly one 0 found in the middle of the run length
    this position will be added to a list of moves.

    run_length refers to the length of values we are checking each loop.

    is_counter is a boolean to identify whether or not we are checking connected values of the opposing player or ours.
    If is_counter is true then the method will search for connections of the opposing identity, it will search ours if 
    false.

    Moves is the list of moves

    board is the current state of the game board.
    """

    def rowGap(self, board, run_length, moves, is_counter):
        identity = self.ID
        if is_counter:
            if self.ID == 1:
                identity = -1

        position = (-1, -1)
        board_size = board.shape[0]
        for r in range(board_size):
            for c in range(board_size - run_length + 1):
                count = 0
                for i in range(run_length):
                    # checks that neither value at either end of the search is a 0
                    if board[r, c + run_length - 1] == 0 or board[r, c] == 0:
                        break
                    # Adds moves to the list if they are 0 and there is only one found on any given loop.
                    if board[r, c + i] != identity and count < 2:
                        count += 1
                        position = (r, c + i)

                if 2 > count > 0:
                    if board[position] == 0:
                        moves.append(position)
        return moves

    """
    Diag Gap produces all positions that a gap is formed in a run of values found diagonally (Either a run of 1s or -1s).
    It loops through all the acceptable positions on the board checking all positions (up to the run length) diagonally
    from that position. If in the run of values there is exactly one 0 found in the middle of the run length
    this position will be added to a list of moves.

    run_length refers to the length of values we are checking each loop.

    is_counter is a boolean to identify whether or not we are checking connected values of the opposing player or ours.
    If is_counter is true then the method will search for connections of the opposing identity, it will search ours if 
    false.

    Moves is the list of moves

    board is the current state of the game board.
    """

    def diagGap(self, board, run_length, moves, is_counter):
        identity = self.ID
        if is_counter:
            if self.ID == 1:
                identity = -1
        position = (-1, -1)
        board_size = board.shape[0]
        for r in range(board_size - run_length + 1):
            for c in range(board_size - run_length + 1):
                count = 0
                for i in range(run_length):
                    # checks that neither value at either end of the search is a 0
                    if board[r + run_length - 1, c + run_length - 1] == 0 or board[r, c] == 0:
                        break
                    # Adds moves to the list if they are 0 and there is only one found on any given loop.
                    if board[r + i, c + i] != identity and count < 2:
                        count += 1
                        position = (r + i, c + i)
                if 2 > count > 0:
                    if board[position] == 0:
                        moves.append(position)
        return moves

    """
    Check will return a list of positions that can be used as moves on a board. This method will make use of the methods
    diag enders, diag gap, row enders and row gap, forming a list of moves. In order to gain all potential moves it will
    run these methods on the board in its current position and on the board to a 90 degree angle. For example the row 
    enders method on the board tilted 90 degrees will produce the moves found in the columns. The method also ensures 
    all positions pulled from boards on an angle are translated properly back to the original board.

    run_length refers to the length of values we are checking which is passed in to each method

    is_counter is a boolean to identify whether or not we are getting a list of attacks or counters.

    board is the current state of the game board.
    """

    def lineCheck(self, board, run_length, is_counter):
        board_rot = np.rot90(np.array(board))
        moves = []
        rot_moves = []
        self.diag_enders(board, run_length, moves, is_counter)
        self.diag_enders(board_rot, run_length, rot_moves, is_counter)
        self.row_enders(board, run_length, moves, is_counter)
        self.row_enders(board_rot, run_length, rot_moves, is_counter)

        self.rowGap(board, run_length + 1, moves, is_counter)
        self.rowGap(board_rot, run_length + 1, rot_moves, is_counter)
        self.diagGap(board, run_length + 1, moves, is_counter)
        self.diagGap(board_rot, run_length + 1, rot_moves, is_counter)

        # Method for translating all of the moves from the rotated board to the regular board.
        for move in rot_moves:
            board_rot_temp = np.array(board_rot)
            board_rot_temp[move] = 5
            board_rot_temp = np.rot90(board_rot_temp, 3)
            np_move = np.where(board_rot_temp == 5)
            true_move = (np_move[0][0], np_move[1][0])
            if true_move not in moves:
                moves.append(true_move)
        return moves
