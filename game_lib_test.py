from game_lib import init_game, game_over, input_check, update_board, wins, ties, score_evaluation, minimax
from math import inf

def test_init_game():
    board, depth = init_game()
    assert depth == 9
    for row in range (3):
        for col in range(3):
            assert board[row][col] == ' '

def test_input_check_correct():
    x = '0'
    y = '1'
    result = input_check(x,y)
    assert result == [0,1]

# TODO: Should test branch coverage 
def test_input_check_out_of_range():
    x = '3'
    y = '1'
    result = input_check(x,y)
    assert result == [-1,-1]

def test_input_check_exception():
    x = ">////<"
    y = "2"
    result = input_check(x,y)
    assert result == [-1,-1]

def test_wins_cols():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[0][0] = board[1][0] = board[2][0] = 'x'
    result = wins(board, 'x')
    assert result == True

def test_wins_rows():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[0][0] = board[0][1] = board[0][2] = 'x'
    result = wins(board, 'x')
    assert result == True

def test_wins_left_diagonals():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[0][0] = board[1][1] = board[2][2] = 'x'
    result = wins(board, 'x')
    assert result == True

def test_wins_right_diagonals():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[2][0] = board[1][1] = board[0][2] = 'x'
    result = wins(board, 'x')
    assert result == True

def test_wins_no_winner():
    board = [[' ' for j in range (3)] for i in range(3)]
    result = wins(board, 'x')
    assert result == False 

def test_ties():
    board = [['x' for j in range (3)] for i in range(3)]
    result = ties(board)
    assert result == True

def test_ties_false():
    board = [[' ' for j in range (3)] for i in range(3)]
    result = ties(board)
    assert result == False

# TODO: Should test branch coverage 
def test_game_over():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[0][0] = board[1][1] = board[2][2] = 'x'
    result = game_over(board)
    assert result == True

def test_game_over_false():
    board = [[' ' for j in range (3)] for i in range(3)]
    result = game_over(board)
    assert result == False

def test_score_evaluation_bot():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[0][0] = board[1][1] = board[2][2] = 'o'
    result = score_evaluation(board, 6)
    assert result == 7

def test_score_evaluation_player():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[0][0] = board[1][1] = board[2][2] = 'x'
    result = score_evaluation(board, 6)
    assert result == -7

def test_score_evaluation_tie():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[0][0] = board[1][1] = board[2][1] = board[1][2] = 'x'
    board[0][1] = board[0][2] = board[1][0] = board[2][0] = board[2][2] = 'o'
    result = score_evaluation(board, 0)
    assert result == 0

def test_minimax():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[0][0] = 'x'
    result = minimax(board, 8, -inf, inf, True)
    assert result[0] == 1
    assert result[1] == 1

def test_update_board_placed():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[0][0] = 'x'
    result = update_board(board, 8, 0, 0)
    assert result[0] == board
    assert result[1] == 8
    assert result[2] == -1

def test_update_board_updated():
    board = [[' ' for j in range (3)] for i in range(3)]
    result = update_board(board, 9, 0, 0)
    assert result[0][1][1] == 'o'
    assert result[1] == 7
    assert result[2] == 0

def test_update_board_human():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[0][0] = board[1][1] = 'x'
    result = update_board(board, 7, 2, 2)
    assert result[0][2][2] == 'x'
    assert result[1] == 6
    assert result[2] == 'x'

def test_update_board_bot():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[2][1] = board[1][2] = 'x'
    board[0][1] = board[0][2] = board[1][0] = board[2][0] = board[2][2] = 'o'
    result = update_board(board, 2, 1, 1)
    assert result[0][0][0] == 'o'
    assert result[1] == 0
    assert result[2] == 'o'

def test_update_board_ties():
    board = [[' ' for j in range (3)] for i in range(3)]
    board[2][1] = board[1][2] = board[0][2] = 'x'
    board[0][1] = board[1][0] = board[2][0] = board[2][2] = 'o'
    result = update_board(board, 2, 0, 0)
    assert result[0][0][0] == 'x'
    assert result[1] == 0
    assert result[2] == 1