from game_lib import game_over, input_check, wins, ties

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