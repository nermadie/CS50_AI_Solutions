"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    board: arr2d
    """
    xCount = 0
    oCount = 0
    for row in board:
        for cell in row:
            if cell == X:
                xCount += 1
            elif cell == O:
                oCount += 1
    return O if xCount > oCount else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    availableAction = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                availableAction.add((i, j))
    return availableAction


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    action: (i, j)
    """
    curPlayer = player(board)
    board[action[0]][action[1]] = curPlayer
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    result = utility(board)
    if result == 1:
        return X
    elif result == -1:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if len(actions(board)) == 0:
        return True
    return utility(board) != 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winConditions = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
        [1, 5, 9],
        [3, 5, 7],
    ]
    for winCondition in winConditions:
        firstCell = board[(winCondition[0] - 1) // 3][(winCondition[0] - 1) % 3]
        secondCell = board[(winCondition[1] - 1) // 3][(winCondition[1] - 1) % 3]
        thirdCell = board[(winCondition[2] - 1) // 3][(winCondition[2] - 1) % 3]
        if firstCell == secondCell and secondCell == thirdCell and firstCell != None:
            return 1 if firstCell == X else -1
    return 0


def minimax(board):
    """
    Trả về nước đi tối ưu cho người chơi hiện tại trên bảng.
    """
    curPlayer = player(board)
    isMax = curPlayer == X
    bestMove, _, _ = minimax_processing(board, 0, isMax)
    return bestMove


def minimax_processing(board, curDepth, isMax):
    """
    Trả về nước đi tối ưu cho người chơi hiện tại trên bảng.
    """
    if terminal(board):
        return None, utility(board), curDepth

    bestMove = None
    bestScore = None
    bestDepth = None

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                board[i][j] = player(board)
                _, score, depth = minimax_processing(board, curDepth + 1, not isMax)
                if bestMove == None:
                    bestMove = (i, j)
                    bestScore = score
                    bestDepth = depth
                else:
                    if isMax and score > bestScore:
                        bestScore = score
                        bestMove = (i, j)
                    elif not isMax and score < bestScore:
                        bestScore = score
                        bestMove = (i, j)
                    elif score == bestScore:
                        if isMax and score == 1 and depth < bestDepth:
                            bestMove = (i, j)
                            bestDepth = depth
                        elif isMax and score != 1 and depth > bestDepth:
                            bestMove = (i, j)
                            bestDepth = depth
                        elif not isMax and score == -1 and depth < bestDepth:
                            bestMove = (i, j)
                            bestDepth = depth
                        elif not isMax and score != -1 and depth > bestDepth:
                            bestMove = (i, j)
                            bestDepth = depth

                board[i][j] = EMPTY
                if curDepth == 0:
                    print((i, j), score, depth)
    if curDepth == 0:
        print()
    return bestMove, bestScore, bestDepth
