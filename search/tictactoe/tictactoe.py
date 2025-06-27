"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for x in range(3):
        for y in range(3):
            if board[x][y]!= EMPTY:
                count += 1

    if count %2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid Action")
    
    new_board = copy.deepcopy(board)
    i,j = action
    new_board[i][j] = player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winning_lines = [
        # Rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],

        # Columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],

        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]
    for line in winning_lines:
        values = [board[i][j] for i, j in line]
        if values == [X, X, X]:
            return X
        if values == [O, O, O]:
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current = player(board)

    def max_value(state):
        if terminal(state):
            return utility(state), None
        v = -math.inf
        best_action = None
        for action in actions(state):
            min_v, _ = min_value(result(state, action))
            if min_v > v:
                v = min_v
                best_action = action
        return v, best_action

    def min_value(state):
        if terminal(state):
            return utility(state), None
        v = math.inf
        best_action = None
        for action in actions(state):
            max_v, _ = max_value(result(state, action))
            if max_v < v:
                v = max_v
                best_action = action
        return v, best_action

    if current == X:
        _, action = max_value(board)
    else:
        _, action = min_value(board)
    return action
