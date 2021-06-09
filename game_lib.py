from math import inf

def init_game ():
    board = [[' ' for j in range (3)] for i in range(3)]
    free_pos = 9
    return board, free_pos

def input_check(arg1, arg2):
    try:
        x = int(arg1)
        y = int(arg2)
        if  0 <= x <= 2 and 0 <= y <= 2:
            return [x, y]
        return [-1, -1]
    except ValueError:
        return [-1, -1]

# One day I will do this smartly using magic number
def wins(board, player):
    for i in range(3):
        # Check row 
        if (board[i][0] == board[i][1] == board[i][2] == player):
            return True
        # Check col
        if (board[0][i] == board[1][i] == board[2][i] == player):
            return True
    # Check Diagonal
    if (board[0][0] == board[1][1] == board[2][2] == player):
        return True
    if(board[2][0] == board[1][1] == board[0][2] == player):
        return True
    return False
     
def ties(board):
    for i in range(3):  
        for j in range(3):
            if board[i][j] == ' ':
                return False
    return True

# Maybe rewrite to return the player
def game_over(board):
    if wins(board, 'x') or wins(board, 'o') or ties(board):
        return True
    return False

# Minimax Collection
# adding depth to score allows it to find the optimal move on any given board
def score_evaluation(board, depth):
    if wins(board, 'o'):
        return  1 + depth
    elif wins(board, 'x'):
        return -1 - depth
    else:
        return 0

# Minimax with alpha beta
def minimax(board, depth, alpha, beta, isMax):
    # Score is in the form of [pos_x, pos_y, score]
    if isMax :
        bestScore = [-1, -1, -inf]
    else:
        bestScore = [-1, -1, inf]

    if game_over(board) or depth == 0:
        score = score_evaluation(board, depth)
        return [-1, -1, score]

    for i in range(3):
        for j in range(3):
            if (board[i][j] == ' '):
                board[i][j] = 'o' if isMax else 'x'
                score = minimax(board, depth-1, alpha, beta, not isMax)
                board[i][j] = ' '
                score[0], score[1] = i, j
                if isMax:
                    if score[2] > bestScore[2]:
                        bestScore = score
                    if bestScore[2] >= beta:
                        return bestScore
                    if bestScore[2] > alpha:
                        alpha = bestScore[2]
                else:
                    if score[2] < bestScore[2]:
                        bestScore = score
                    if bestScore[2] <= alpha:
                        return bestScore
                    if bestScore[2] < beta:
                        beta = bestScore[2]
                
    #print([board,depth,isMax,bestScore])
    return bestScore

'''
return [board, depth, win]
'''
def update_board(board, depth, x, y):
    if (board[x][y] != ' '):
        return [board, depth, -1]

    board[x][y] = 'x'
    depth -= 1

    if wins(board, "x"):
        return [board, depth, 'x']

    bot_move = minimax(board, depth, -inf, inf, True)

    if bot_move[0] != -1:
        board[bot_move[0]][bot_move[1]] = 'o'
        depth -= 1

    if wins(board, "o"):
            return [board, depth, 'o']

    if ties(board):
        return [board, depth, 1]

    return [board, depth, 0]