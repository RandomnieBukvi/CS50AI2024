"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

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
    x_count = 0
    o_count = 0
    for row in board:
        for col in row:
            if col == X:
                x_count += 1
            elif col == O:
                o_count += 1
    player_sign = X if x_count == o_count else O
    return player_sign


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == EMPTY:
                all_actions.add((i, j))
    return all_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    action_i = action[0]
    action_j = action[1]
    player_sign = player(board)
    if 0 <= action_i < 3 and 0 <= action_j < 3 and board[action_i][action_j] == EMPTY:
        new_board = deepcopy(board)
        new_board[action_i][action_j] = player_sign
        return new_board
    else:
        raise Exception("Invalid acton")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # horizontal check
    for row in board:
        if row[0] != EMPTY and row[0] == row[1] == row[2]:
            return row[0]
    # print(board)
    # print("h check done")
    # vertical check
    for i in range(3):
        if board[0][i] != EMPTY and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
    # print(board)
    # print("v check done")
    # diagonal check
    if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[2][0] != EMPTY and board[2][0] == board[1][1] == board[0][2]:
        return board[2][0]
    # print(board)
    # print("d check done")
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # print(winner(board))
    if winner(board) is not None or not any(EMPTY in row for row in board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    sign_to_num = {X: 1,
                   O: -1,
                   EMPTY: 0
                   }
    return sign_to_num[winner(board)]

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    actions_list = list(actions(board))
    if player(board) == X:
        actions_results = []
        for action in actions_list:
            actions_results.append(min_value(result(board, action), -999, 999))
        desired_action_index = actions_results.index(max(actions_results))
        return actions_list[desired_action_index]
    else:
        actions_results = []
        for action in actions_list:
            actions_results.append(max_value(result(board, action), -999, 999))
        desired_action_index = actions_results.index(min(actions_results))
        return actions_list[desired_action_index]


def max_value(board, alpha, beta):
    max_val = -999
    if terminal(board):
        return utility(board)
    for action in actions(board):
        val = min_value(result(board, action), alpha, beta)
        max_val = max(max_val, val)
        alpha = max(alpha, val)
        if beta <= alpha:
            break
    return max_val


def min_value(board, alpha, beta):
    min_val = 999
    if terminal(board):
        return utility(board)
    for action in actions(board):
        val = max_value(result(board, action), alpha, beta)
        min_val = min(min_val, val)
        beta = min(beta, val)
        if beta <= alpha:
            break
    return min_val

