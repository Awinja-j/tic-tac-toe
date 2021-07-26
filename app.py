from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
import random

app = Flask(__name__)


board = ['.','.','.','.','.','.','.','.','.']

human_player_board = list()

continue_with_game = True # will be false if we have a tie or win

winner = None # is none until winner is found, then 1

current_player = None

def display_board():
    '''
    This displays the board on the screen
    '''
    global board

    print(board[0],board[1],board[2])
    print(board[3],board[4],board[5])
    print(board[6],board[7],board[8])

def play_game(human_player_board):
    '''
    play game
    '''
    print(human_player_board, 'hhhhh')

    # 1: if this game has not been won, then keep looping until wel get a winner!

    while continue_with_game:

            # human is in control of this game
            human_player()
        
    # when the game has been won, then we get out of the loop and print the winner
    if winner == "x" or winner == "o":
        return jsonify({"and the winner is": winner})
    elif winner == None:
        return jsonify({"its a tie": display_board()})

def computer_play():
    print('computer is here there')

    # Handle a turn
    computer_turn()

    # Check if the game is over
    check_if_game_over()

    # Flip to the other player
    flip_player()

    return jsonify({'your turn':display_board()})

def human_player():

    # Handle a turn
    human_turn()

    # Check if the game is over
    check_if_game_over()

    # Flip to the other player
    flip_player()

    #after it is done playing, call computer to play
    computer_play()

def computer_turn():
    global board
    n = random.randint(0,9)
    if board[n] == '.':
        board[n] = 'o'

# def human_turn():
#     position = get_new_position()
#     print('nnnn', position)

#     if position == False:
        

#     # Put the game piece on the board
#     board[int(position)] = 'x'

def human_turn():

    global board, human_player_board

    for k,v in enumerate(human_player_board):
        if board[k] == '.':
            board[int(k)] = 'x'
        else:
            raise BadRequest('This position has been played')


# Check if the game is over
def check_if_game_over():
    check_for_winner()
    check_for_tie()


# Check to see if somebody has won
def check_for_winner():
    '''
    Checks if there is a winner in rows, columns or in the two diagonals
    '''
    row_winner = check_rows()
    column_winner = check_columns()
    diagonal_winner = check_diagonals()

    if row_winner:
        winner = row_winner
    elif column_winner:
        winner = column_winner
    elif diagonal_winner:
        winner = diagonal_winner
    else:
        winner = None


def check_rows():
    global board
    # Check if any of the rows have all the same value (and is not empty)
    row_1 = board[0] == board[1] == board[2] != "."
    row_2 = board[3] == board[4] == board[5] != "."
    row_3 = board[6] == board[7] == board[8] != "."
    # If any row does have a match, flag that there is a win
    if row_1 or row_2 or row_3:
        continue_with_game = False
    # Return the winner
    if row_1:
        return board[0] 
    elif row_2:
        return board[3] 
    elif row_3:
        return board[6] 
    # Or return None if there was no winner
    else:
        return None

# Check the columns for a win
def check_columns():
    global board
    # Check if any of the columns have all the same value (and is not empty)
    column_1 = board[0] == board[3] == board[6] != "."
    column_2 = board[1] == board[4] == board[7] != "."
    column_3 = board[2] == board[5] == board[8] != "."
    # If any row does have a match, flag that there is a win
    if column_1 or column_2 or column_3:
        continue_with_game = False
    # Return the winner
    if column_1:
        return board[0] 
    elif column_2:
        return board[1] 
    elif column_3:
        return board[2] 
    # Or return None if there was no winner
    else:
        return None


def check_diagonals():
    global board
    # Check if any of the columns have all the same value (and is not empty)
    diagonal_1 = board[0] == board[4] == board[8] != "."
    diagonal_2 = board[2] == board[4] == board[6] != "."
    # If any row does have a match, flag that there is a win
    if diagonal_1 or diagonal_2:
        continue_with_game = False
    # Return the winner
    if diagonal_1:
        return board[0] 
    elif diagonal_2:
        return board[2]
    # Or return None if there was no winner
    else:
        return None


# Check if there is a tie
def check_for_tie():
    global board
    # If board is full
    if "." not in board:
        continue_with_game = False
        return True
    # Else there is no tie
    else:
        return False


# Flip the current player from X to O, or O to X depending on who has played
def flip_player():

    global current_player

    # If the current player was X, make it O
    if current_player == "x":
        current_player = "o"
    # Or if the current player was O, make it X
    elif current_player == "o":
        current_player = "x"


@app.route("/", methods=['GET'])
def index():
    board = request.args.get('board')
    if not board:
        raise BadRequest('Missing board')

    if isinstance(board, str) is False:
        raise BadRequest('Board must be in string format')

    if len(board) > 9:
        raise BadRequest('Board cannot be more than 9 characters')

    board = list(board)

    game = play_game(board)

    return game()
