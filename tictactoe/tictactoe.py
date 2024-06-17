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
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O



def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    i, j = action
    if board[i][j] != EMPTY:
        raise ValueError("Invalid move")
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    lines = [
        board[0], board[1], board[2],  # Rows
        [board[0][0], board[1][0], board[2][0]],  # Columns
        [board[0][1], board[1][1], board[2][1]],  # Columns
        [board[0][2], board[1][2], board[2][2]],  # Columns
        [board[0][0], board[1][1], board[2][2]],  # Diagonals
        [board[0][2], board[1][1], board[2][0]]
    ]

    for line in lines:
        if line[0] == line[1] == line[2] and line[0] is not EMPTY:
            return line[0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


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
    def max_value(board):
        if terminal(board):
            return utility(board)
        value = -math.inf
        for action in actions(board):
            value = max(value, min_value(result(board, action)))
        return value

    def min_value(board):
        if terminal(board):
            return utility(board)
        value = math.inf
        for action in actions(board):
            value = min(value, max_value(result(board, action)))
        return value

    if terminal(board):
        return None

    current_player = player(board)
    best_action = None
    if current_player == X:
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action

    return best_action
