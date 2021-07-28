from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
import random

app = Flask(__name__)

#!/usr/bin/env python3
from math import inf as infinity
from random import choice

HUMAN = -1
COMP = +1

def evaluate(state):
    
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y, game_board):
    
    board = game_board
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player, game_board):
    
    board = game_board
    if valid_move(x, y, board):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]


    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

def computer_turn(game_board: list) -> list:
    board = game_board
    depth = len(empty_cells(board))  #number of empty cells

    if depth == 0 or game_over(board): #if there isnt any, end game
        return

    if depth == 9: # if the board has not been played...
        x = choice([0, 1, 2]) # randomly choose from the three ints and set
        y = choice([0, 1, 2]) # randomly choose from the three ints and set
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    h = set_move(x, y, COMP, game_board) # to the gameboard, set the choices

    if h == True:
        return game_board

def main(game_board: list) -> list:
    """
    We assume that the human has played when a board is passed
    when the board is passed as [[0,0,0],[0,0,0],[0,0,0]], this means human has 
    not played and computer needs to play first.
    """

    if len(empty_cells(game_board)) == 0: # if the board does not have any empty spaces, just return the board as is
        return game_board

    return computer_turn(game_board) # otherwise computer will play

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

    board = list(divide_to_chunks(board, 3))

    game = main(board)

    print('gmae', game)

    game_results = change_to_string(game)

    return game_results

def change_to_nums(list_items):
    for k,v in enumerate(list_items):
        if v == 'x':
            list_items[k] = -1
        elif v == 'o':
            list_items[k] = +1
        elif v.isspace() == True:
            list_items[k] = 0
    return list_items

def divide_to_chunks(j,n):
    l = change_to_nums(j)
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def change_back(x):
    for k,v in enumerate(x): 
        if v == 1:
            x[k] = 'o'
        elif v == -1:
            x[k] = 'x'
        elif v == 0:
            x[k] = ''
    return x

def change_to_string(t):
    flat_list = [item for sublist in t for item in sublist]
    n = change_back(flat_list)
    m = ' '.join([str(elem) for elem in n])

    return m