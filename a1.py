# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a1.html

import sys
import random

class BinaryGame:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.board = [['.'] * width for _ in range(height)]
        self.last_player = None

    def is_valid_move(self, x, y, digit):
        '''
        Checks if the move is valid or not
        
        :param x: the x-coordinate
        :type x: str
        :param y: the y-coordinate
        :type y: str
        :param digit: the player number
        :type digit: str
        :return: the tuple with the first item is whether the move is valid/legal and the second item is the reason for invalid/illegal move or None if the move is valid/legal
        :rtype: Tuple[bool, str]
        '''

        # Check if the x and y coordinates are valid
        if not x.isnumeric() or not y.isnumeric() or int(x) < 0 or int(x) >= self.width or int(y) < 0 or int(y) >= self.height:
            return (False, "wrong coordinate")
        x = int(x)
        y = int(y)

        # Check if the digit is valid (0 or 1)
        if not digit.isnumeric() or int(digit) not in [0, 1]:
            return (False, "wrong number")
        digit = int(digit)

        # Check if the specified cell is occupied
        if self.board[y][x] != '.':
            return (False, "occupied")

        # Check if the move violates the triple constraint
        if not self.check_triples_constraint(x, y, digit):
            return (False, "three in a row")

        # Check if the move violates the balance constraint
        if not self.check_balance_constraint(x, y, digit):
            return (False, "too many 0") if digit == 0 else (False, "too many 1")

        return (True, None)

    def check_triples_constraint(self, x, y, digit):
        # Check row
        row = ''.join(self.board[y][:x] + [str(digit)] + self.board[y][x+1:])
        if '000' in row or '111' in row:
            return False
        # Check column
        col = ''.join([self.board[i][x] for i in range(self.height)])
        col = col[:y] + str(digit) + col[y+1:]
        if '000' in col or '111' in col:
            return False
        return True

    def check_balance_constraint(self, x, y, digit):
        # Check row
        row = self.board[y][:x] + [str(digit)] + self.board[y][x+1:]
        zeros = row.count('0')
        ones = row.count('1')
        if zeros > (self.width + 1) // 2 or ones > (self.width + 1) // 2:
            return False
        # Check column
        col = [self.board[i][x] for i in range(self.height)]
        col = col[:y] + [str(digit)] + col[y+1:]
        zeros = col.count('0')
        ones = col.count('1')
        if zeros > (self.height + 1) // 2 or ones > (self.height + 1) // 2:
            return False
        return True

    def make_move(self, x, y, digit):

        valid_move, reason = self.is_valid_move(x, y, digit)
        if valid_move:
            self.board[int(y)][int(x)] = str(digit)
            if self.last_player == None:
                self.last_player = 1
            else:
                self.last_player = 3 - self.last_player
            return (True, None)
            
        return (False, reason)

    def get_legal_moves(self):
        moves = []
        for y in range(self.height):
            for x in range(self.width):
                for digit in ['0', '1']:
                    if self.is_valid_move(str(x), str(y), digit)[0]:
                        moves.append((x, y, int(digit)))

        return moves

    def is_game_over(self):

        return len(self.get_legal_moves()) == 0

    def get_winner(self):

        if self.is_game_over():
            return self.last_player
        return None

class CommandInterface:
    # The following is already defined and does not need modification
    # However, you may change or add to this code as you see fit, e.g. adding class variables to init

    def __init__(self):
        # Define the string to function command mapping
        self.game = None
        self.command_dict = {
            "help" : self.help,
            "game" : self.game_cmd,
            "show" : self.show,
            "play" : self.play,
            "legal" : self.legal,
            "genmove" : self.genmove,
            "winner" : self.winner
        }

    # Convert a raw string to a command and a list of arguments
    def process_command(self, str):
        str = str.lower().strip()
        command = str.split(" ")[0]
        args = [x for x in str.split(" ")[1:] if len(x) > 0]
        if command not in self.command_dict:
            print("? Unknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            print("Command '" + str + "' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False
        
    # Will continuously receive and execute commands
    # Commands should return True on success, and False on failure
    # Commands will automatically print '= 1' at the end of execution on success
    def main_loop(self):
        while True:
            str = input()
            if str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(str):
                print("= 1\n")

    # List available commands
    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    #======================================================================================
    # End of predefined functionality. You will need to implement the following functions.
    # Arguments are given as a list of strings
    # We will only test error handling of the play command
    #======================================================================================

    def game_cmd(self, args):
        if len(args) != 2:
            raise ValueError("'game' command requires 2 arguments: width and height")
        width, height = map(int, args)
        if width < 1 or width > 20 or height < 1 or height > 20:
            raise ValueError("Width and height must be between 1 and 20")
        self.game = BinaryGame(width, height)
        return True
    
    def show(self, args):
        if self.game is None:
            raise ValueError("No game in progress. Use 'game' command to start a new game.")
        for row in self.game.board:
            print(''.join(row))
        return True
    
    def play(self, args):
        # Check if there is an exiting game
        if self.game is None:
            raise ValueError("No game in progress. Use 'game' command to start a new game.")
        
        # Check if the play command has exactly 3 arguments
        if len(args) != 3:
            print(f"= illegal move: " + ' '.join(args) + " wrong number of arguments")
            return False

        # Play the move if valid, otherwise output error message
        x, y, digit = str(args[0]), str(args[1]), str(args[2])
        valid_move, reason = self.game.make_move(x, y, digit)
        if not valid_move:
            print(f"= illegal move: {x} {y} {digit} " + reason)
            return False

        return True
    
    def legal(self, args):
        if self.game is None:
            raise ValueError("No game in progress. Use 'game' command to start a new game.")
        x, y, digit = str(args[0]), str(args[1]), str(args[2])
        print("yes" if self.game.is_valid_move(x, y, digit)[0] else "no")
        return True
    
    def genmove(self, args):
        if self.game is None:
            raise ValueError("No game in progress. Use 'game' command to start a new game.")
        legal_moves = self.game.get_legal_moves()
        if not legal_moves:
            print("resign")
        else:
            x, y, digit = random.choice(legal_moves)
            self.game.make_move(str(x), str(y), str(digit))
            print(f"{x} {y} {digit}")

        return True
    
    def winner(self, args):
        if self.game is None:
            raise ValueError("No game in progress. Use 'game' command to start a new game.")
        winner = self.game.get_winner()
        if winner is None:
            print("unfinished")
        else:
            print(winner)
        return True
    
    #======================================================================================
    # End of functions requiring implementation
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()