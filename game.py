from player import HumanPlayer, RandomComputerPlayer, OptimalComputerPlayer
import time

class TicTacToe:
    def __init__(self):
        # list of length 9 to represent 3x3 board
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        moves = []
        for (i, spot) in enumerate(self.board):
            # assign symbol to space index using tuples
            if spot == ' ':
                moves.append(i)
        return moves
        # below line does same as above
        # return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return len(self.available_moves())

    def make_move(self, square, symbol):
        if self.board[square] == ' ':
            self.board[square] = symbol
            # check for winner
            if self.winner(square, symbol):
                self.current_winner = symbol
            return True
        return False

    def winner(self, square, symbol):
        # win con
        row_ind = square // 3
        row = self.board[row_ind * 3: (row_ind + 1) * 3]
        if all([spot == symbol for spot in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == symbol for spot in column]):
            return True

        # observation: all diagonal spot indices are even numbers
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == symbol for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == symbol for spot in diagonal2]):
                return True

        return False


def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    symbol = 'X'  # starting symbol
    # iterate while there are empty spots remaining
    while game.empty_squares():
        # get move from the right player
        if symbol == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, symbol):
            if print_game:
                print(symbol + f' makes a move to square {square}')
                game.print_board()
                print('')

                if game.current_winner:
                    if print_game:
                        print(symbol + ' has achieved victory!')
                    return symbol

                # change symbol after move
                if symbol == 'X':
                    symbol = 'O'
                else:
                    symbol = 'X'

            time.sleep(0.4)

    if print_game:
        print('Tie!')

def choose_bot():
    print('1. Random CPU')
    print('2. Optimal CPU using Minimax')
    c = 0
    while c != 1 and c != 2:
        c = int(input('Your choice: '))
    return c

if __name__ == '__main__':

    print('1. Go first as X')
    print('2. Go second as O')
    print('3. Watch 2 bots duke it out')

    choice = int(input('Your choice (1/2/3): '))
    if choice==1:
        x_player = HumanPlayer('X')
        c = choose_bot()
        if c==1: o_player = RandomComputerPlayer('O')
        elif c==2: o_player = OptimalComputerPlayer('O')

    elif choice==2:
        o_player = HumanPlayer('O')
        c = choose_bot()
        if c==1: x_player = RandomComputerPlayer('X')
        elif c==2: x_player = OptimalComputerPlayer('X')

    elif choice==3:
        x_player = OptimalComputerPlayer('X')
        o_player = OptimalComputerPlayer('O')

    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)
