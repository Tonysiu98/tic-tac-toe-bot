#import random
from math import inf

# Initialise the board 
# board[row][col]
board = [[' ' for j in range (3)] for i in range(3)]
free_pos = 9

# Initialise Game info
current_player = None

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
     
def ties():
    global board
    for i in range(3):  
        for j in range(3):
            if board[i][j] == ' ':
                return False
    return True

# Maybe rewrite to return the player
def game_over(board):
    if wins(board, 'x') or wins(board, 'o') or ties():
        return True
    return False

async def print_board(ctx):
    global board
    await ctx.send("{}  |  {}  |  {}\n {}  |  {}  |  {}\n {}  |  {}  |  {}"
        .format(board[0][0], board[0][1], board[0][2],board[1][0], board[1][1], board[1][2],board[2][0], board[2][1], board[2][2]))

def reset_game():
    global board, free_pos, current_player
    board = [[' ' for j in range (3)] for i in range(3)]
    free_pos = 9
    current_player = None

# Minimax Collection
def score_evaluation(board):
    if wins(board, 'o'):
        score = 1
    elif wins(board, 'x'):
        score = -1
    else:
        score = 0
    return score


def minimax(board, depth, isMax):
    # Score is in the form of [pos_x, pos_y, score]
    if isMax :
        bestScore = [-1, -1, -inf]
    else:
        bestScore = [-1, -1, inf]

    if depth == 0 or game_over(board):
        score = score_evaluation(board)
        return [-1, -1, score]

    for i in range(3):
        for j in range(3):
            if (board[i][j] == ' '):
                board[i][j] = 'o' if isMax else 'x'
                score = minimax(board, depth-1, not isMax)
                board[i][j] = ' '
                score[0], score[1] = i, j
                if isMax:
                    if score[2] > bestScore[2]:
                        bestScore = score
                else:
                    if score[2] < bestScore[2]:
                        bestScore = score
    return bestScore

def best_move(board, depth):
    best_score = -inf
    move = [-1,-1]
    for i in range(3):
        for j in range(3):
            if (board[i][j] == ' '):
                current_score = minimax(board, depth, True)
                board[i][j] == ' '
                if (current_score[2] > best_score):
                    best_score = current_score[2]
                    move[0], move[1] = current_score[0], current_score[1]
    return move

def game():
    global free_pos
    print_board(board)
    while True:
        print("Pick a position")
        pos = input().split(' ')
        board[int(pos[0])][int(pos[1])] = "x"

        print_board(board)

        if wins(board, "x"):
            print_board(board)
            print("Player won")
            return

        free_pos -= 1

        # Random move
        # done = False
        # while(not done):
        #     x = random.randint(0,2)
        #     y = random.randint(0,2)
        #     if(board[x][y] == ' '):
        #         board[x][y] = 'o'
        #         done = True

        x, y = best_move(board, free_pos)
        if (x != -1):
            board[x][y] = 'o'
            free_pos -= 1
        print_board(board)

        if wins(board, "o"):
            print_board(board)
            print("bot won")
            return
     
        if ties(board):
            print_board(board)
            print("game ties")
            return
async def update_board(ctx, x, y):
    global board, free_pos
    if (board[x][y] != ' '):
        await ctx.send("The places is taken, choose another")
        return
    board[x][y] = 'x'
    free_pos -= 1
    await print_board(ctx)

    if wins(board, "x"):
            await print_board(ctx)
            await ctx.send("Player won")
            reset_game()
            return

    bot_move = best_move(board, free_pos)
    print(bot_move)
    if bot_move[0] != -1:
        board[bot_move[0]][bot_move[1]] = 'o'
        free_pos -= 1
    print(board)
    
    await print_board(ctx)

    if wins(board, "o"):
            await print_board(ctx)
            await ctx.send("Bot won")
            reset_game()

    if ties():
        #await print_board(ctx)
        await ctx.send("game ties won")
        reset_game()