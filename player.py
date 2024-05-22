import math
import random

class Player:
    def __init__(self, symbol):
        # symbol X or O
        self.symbol = symbol


    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def get_move(self, game):
        # randomly chooses a spot
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def get_move(self, game):
        # choose depend on input
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.symbol + '\'s turn. Choose move (0-8): ')
            # invalid check: cast to integer, valid if this works
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square, try again')

        return val

class OptimalComputerPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def get_move(self, game):
        # if very first move: go randomly
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.symbol)['position']
        return square

    def minimax(self, state, player):
        maxi = self.symbol
        mini = 'O' if player == 'X' else 'X'

        if state.current_winner == mini:
            return {
                'position': None,
                'score': 1 * (state.num_empty_squares() + 1) if mini == maxi else -1 * (state.num_empty_squares() + 1)
            }

        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == maxi:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            # try a move
            state.make_move(possible_move, player)

            # recurse w/ minimax ot sim a game after that move
            sim_score = self.minimax(state, mini) # alternate players

            # undo made move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            # update dict(minimax values) if needed
            if player == maxi:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best
