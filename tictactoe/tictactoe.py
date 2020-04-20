"""
Tic Tac Toe Player
"""

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


def player(board) -> str:
    """
    Returns player who has the next turn on a board.
    """
    x_amount = 0
    o_amount = 0
    for row in board:
        for column in row:
            if column == X:
                x_amount += 1
            elif column == O:
                o_amount += 1

    return X if x_amount == o_amount else O


def actions(board) -> set:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_actions = set()
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == EMPTY:
                set_actions.add((i, j))
    return set_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    val_at_action = board[action[0]][action[1]]
    if val_at_action != EMPTY:
        raise Exception('invalid action')

    next_board = copy.deepcopy(board)
    next_board[action[0]][action[1]] = player(board)
    return next_board


def winner(board) -> any:
    """
    Returns the winner of the game, if there is one.
    """
    numeric_board = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]]

    total_horizon = [0, 0, 0]
    total_vertical = [0, 0, 0]
    total_diagonally = [0, 0]
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == X:
                numeric_board[i][j] = 1
                total_horizon[i] += 1
                total_vertical[j] += 1
            elif column == O:
                numeric_board[i][j] = -1
                total_horizon[i] += -1
                total_vertical[j] += -1

    n = len(numeric_board)
    total_diagonally[0] = sum(numeric_board[i][i] for i in range(n))
    total_diagonally[1] = sum(numeric_board[i][n - i - 1] for i in range(n))

    if 3 in total_horizon or 3 in total_vertical or 3 in total_diagonally:
        return X
    elif -3 in total_horizon or -3 in total_vertical or -3 in total_diagonally:
        return O
    else:
        return None


def terminal(board) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        for column in row:
            if column == EMPTY:
                return False
    return True


def utility(board) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0


def minimax(board) -> (int, int):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if board == initial_state():
        return 1, 1

    optimal_action = None
    max_v = -1000
    min_v = 1000

    person = player(board)
    if person == X:
        for action in actions(board):
            v = min_value(result(board, action))
            if v > max_v:
                max_v = v
                optimal_action = action
    else:
        for action in actions(board):
            v = max_value(result(board, action))
            if v < min_v:
                min_v = v
                optimal_action = action

    return optimal_action


def max_value(board) -> int:
    if terminal(board):
        return utility(board)
    v = -1000
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board) -> int:
    if terminal(board):
        return utility(board)
    v = 1000
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
