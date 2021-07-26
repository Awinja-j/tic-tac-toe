from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

class TicTacToe:
    def __init__(self, board: list):
        self.board =    [" ", " ", " ",
                        " ", " ", " ",
                        " ", " ", " "]
        
        self.human_player_board = board

        self.continue_with_game = True # will be false if we have a tie or win
        
        self.winner = None # is none until winner is found, then 1

        self.current_player = "o" # who is currently playing?

    # def display_board(self):
    #     '''
    #     This displays the board on the screen
    #     '''
    #     print("\n")
    #     print(self.board[0] + " | " + self.board[1] + " | " + self.board[2] + "     1 | 2 | 3")
    #     print(self.board[3] + " | " + self.board[4] + " | " + self.board[5] + "     4 | 5 | 6")
    #     print(self.board[6] + " | " + self.board[7] + " | " + self.board[8] + "     7 | 8 | 9")
    #     print("\n")

    # Play a game of tic tac toe
    def play_game(self) -> dict:

        # 1: if this game has not been won, then keep looping until wel get a winner!

        while self.continue_with_game:

            # 2: lets check who is currently playing, computer plays as o and human player is x
            player = self.current_player()

            # 3.if the current player is computer, then call self.computer_play()
            if player == "o":
                self.computer_play()
            else: 
                # 3a: human player passes  
                self.human_player()
        
        # when the game has been won, then we get out of the loop and print the winner
        if self.winner == "x" or self.winner == "o":
            return jsonify({"and the winner is": self.winner})
        elif self.winner == None:
            return jsonify({"its a tie": ":-)"})

    def computer_play(self):
        # Handle a turn
        self.computer_turn()

        # Check if the game is over
        self.check_if_game_over()

        # Flip to the other player
        self.flip_player()

    def human_player(self):
        # Handle a turn
        self.human_turn()

        # Check if the game is over
        self.check_if_game_over()

        # Flip to the other player
        self.flip_player()

    def computer_turn(self):
        pass

    # def human_turn(self):

    #     # Get position from player
    #     print(player + "'s turn.")
    #     position = input("Choose a position from 1-9: ")

    #     # Whatever the user inputs, make sure it is a valid input, and the spot is open
    #     valid = False
    #     while not valid:

    #         # Make sure the input is valid
    #         while position not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
    #             position = input("Choose a position from 1-9: ")
        
    #         # Get correct index in our board list
    #         position = int(position) - 1

    #         # Then also make sure the spot is available on the board
    #         if self.board[position] == "-":
    #             valid = True
    #         else:
    #             print("You can't go there. Go again.")

    #     # Put the game piece on the board
    #     self.board[position] = player

    #     # Show the game board
    #     self.display_board()

    # def get_new_human_player_entry(self):
    #     for key, value in enumerate(self.board):
    #         for key
    #     _

    # Check if the game is over
    def check_if_game_over(self):
        self.check_for_winner()
        self.check_for_tie()


    # Check to see if somebody has won
    def check_for_winner(self):
        '''
        Checks if there is a winner in rows, columns or in the two diagonals
        '''
        row_winner = self.check_rows()
        column_winner = self.check_columns()
        diagonal_winner = self.check_diagonals()

        if row_winner:
            self.winner = row_winner
        elif column_winner:
            self.winner = column_winner
        elif diagonal_winner:
            self.winner = diagonal_winner
        else:
            self.winner = None


    def check_rows(self):
        # Check if any of the rows have all the same value (and is not empty)
        row_1 = self.board[0] == self.board[1] == self.board[2] != "-"
        row_2 = self.board[3] == self.board[4] == self.board[5] != "-"
        row_3 = self.board[6] == self.board[7] == self.board[8] != "-"
        # If any row does have a match, flag that there is a win
        if row_1 or row_2 or row_3:
            self.continue_with_game = False
        # Return the winner
        if row_1:
            return self.board[0] 
        elif row_2:
            return self.board[3] 
        elif row_3:
            return self.board[6] 
        # Or return None if there was no winner
        else:
            return None


    # Check the columns for a win
    def check_columns(self):
        # Check if any of the columns have all the same value (and is not empty)
        column_1 = self.board[0] == self.board[3] == self.board[6] != "-"
        column_2 = self.board[1] == self.board[4] == self.board[7] != "-"
        column_3 = self.board[2] == self.board[5] == self.board[8] != "-"
        # If any row does have a match, flag that there is a win
        if column_1 or column_2 or column_3:
            self.continue_with_game = False
        # Return the winner
        if column_1:
            return self.board[0] 
        elif column_2:
            return self.board[1] 
        elif column_3:
            return self.board[2] 
        # Or return None if there was no winner
        else:
            return None


    def check_diagonals(self):
        # Check if any of the columns have all the same value (and is not empty)
        diagonal_1 = self.board[0] == self.board[4] == self.board[8] != "-"
        diagonal_2 = self.board[2] == self.board[4] == self.board[6] != "-"
        # If any row does have a match, flag that there is a win
        if diagonal_1 or diagonal_2:
            self.continue_with_game = False
        # Return the winner
        if diagonal_1:
            return self.board[0] 
        elif diagonal_2:
            return self.board[2]
        # Or return None if there was no winner
        else:
            return None


    # Check if there is a tie
    def check_for_tie(self):
        # If board is full
        if "-" not in self.board:
            self.continue_with_game = False
            return True
        # Else there is no tie
        else:
            return False


    # Flip the current player from X to O, or O to X
    def flip_player(self):
        # If the current player was X, make it O
        if self.current_player == "x":
            self.current_player = "o"
        # Or if the current player was O, make it X
        elif self.current_player == "o":
            self.current_player = "x"

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

    return TicTacToe.play_game(board)

if __name__ == '__main__':
    app.run(debug=True)