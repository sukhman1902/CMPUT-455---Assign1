import random
import sys

class BinaryGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['.'] * width for _ in range(height)]
        self.current_player = 1

    def is_valid_move(self, x, y, digit):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        if self.board[y][x] != '.':
            return False
        if not self.check_triples_constraint(x, y, digit):
            return False
        if not self.check_balance_constraint(x, y, digit):
            return False
        return True

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
        if self.is_valid_move(x, y, digit):
            self.board[y][x] = str(digit)
            self.current_player = 3 - self.current_player  # Switch player
            return True
        return False

    def get_legal_moves(self):
        moves = []
        for y in range(self.height):
            for x in range(self.width):
                for digit in ['0', '1']:
                    if self.is_valid_move(x, y, int(digit)):
                        moves.append((x, y, digit))
        return moves

    def is_game_over(self):
        return len(self.get_legal_moves()) == 0

    def get_winner(self):
        if self.is_game_over():
            return 3 - self.current_player  # The player who made the last move wins
        return None

class CommandInterface:
    def __init__(self):
        self.game = None
        self.command_dict = {
            "help": self.help,
            "game": self.game_cmd,
            "show": self.show,
            "play": self.play,
            "legal": self.legal,
            "genmove": self.genmove,
            "winner": self.winner
        }

    def process_command(self, command_str):
        command_str = command_str.lower().strip()
        command = command_str.split(" ")[0]
        args = [x for x in command_str.split(" ")[1:] if len(x) > 0]
        if command not in self.command_dict:
            print("? Unknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            print(f"Command '{command_str}' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False

    def main_loop(self):
        while True:
            command_str = input()
            if command_str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(command_str):
                print("= 1\n")

    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    def game_cmd(self, args):
        if len(args) != 2:
            raise ValueError("game command requires 2 arguments: width and height")
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
        if self.game is None:
            raise ValueError("No game in progress. Use 'game' command to start a new game.")
        if len(args) != 3:
            raise ValueError("play command requires 3 arguments: x y digit")
        x, y, digit = int(args[0]), int(args[1]), int(args[2])
        if not self.game.make_move(x, y, digit):
            raise ValueError("Illegal move")
        return True

    def legal(self, args):
        if self.game is None:
            raise ValueError("No game in progress. Use 'game' command to start a new game.")
        if len(args) != 3:
            raise ValueError("legal command requires 3 arguments: x y digit")
        x, y, digit = int(args[0]), int(args[1]), int(args[2])
        print("yes" if self.game.is_valid_move(x, y, digit) else "no")
        return True

    def genmove(self, args):
        if self.game is None:
            raise ValueError("No game in progress. Use 'game' command to start a new game.")
        legal_moves = self.game.get_legal_moves()
        if not legal_moves:
            print("resign")
        else:
            x, y, digit = random.choice(legal_moves)
            self.game.make_move(x, y, int(digit))
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

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()