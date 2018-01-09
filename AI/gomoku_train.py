from random import choice
from genetic import Genetic

class Gomoku():
    def __init__(self):
        self.board = [0 for _ in range(225)]

    def restart(self):
        self.board = [0 for _ in range(225)]

    def get_board(self):
        return self.board

    def get_empty_pos(self):
        return [index for index, value in enumerate(self.get_board()) if value == 0]

    def add_piece(self, player, move):
        if move in self.get_empty_pos():
            self.board[move] = player

    def is_over(self):
        board = self.get_board()

        for i in range(15):
            for j in range(15):
                if board[i * 15 + j] != 0 and i * 15 + j + 4 * 1 < 225 and len(set([board[i * 15 + j + k * 1] for k in range(5)])) == 1:
                    return True, board[i * 15 + j]
                elif board[i * 15 + j] != 0 and i * 15 + j + 4 * 16 < 225 and len(set([board[i * 15 + j + k * 16] for k in range(5)])) == 1:
                    return True, board[i * 15 + j]
                elif board[i * 15 + j] != 0 and i * 15 + j + 4 * 14 < 225 and len(set([board[i * 15 + j + k * 14] for k in range(5)])) == 1:
                    return True, board[i * 15 + j]
                elif board[i * 15 + j] != 0 and i * 15 + j + 4 * 15 < 225 and len(set([board[i * 15 + j + k * 15] for k in range(5)])) == 1:
                    return True, board[i * 15 + j]
        if len(self.get_empty_pos()) == 0:
            return True, 0
        return False, 0

    def __str__(self):
        board = ['X' if x == 1 else x for x in self.board]
        board = ['O' if x == -1 else x for x in board]
        board = ['.' if x == 0 else x for x in board]
        return '\n'.join(' | '.join(board[i * 15 + j] for j in range(15)) for i in range(15))

class GomukuAgent():
    def __init__(self, player):
        self.player = player 

    def get_player(self):
        return self.player

    def next_move(self, game, print_board = False):
        empty_positions = game.get_empty_pos()
        mov = choice(empty_positions)
        game.add_piece(self.get_player(), mov)

        if print_board:
            print(game)

        return mov

class GomukuGeneticAgent(GomukuAgent):
    def __init__(self, player):
        super().__init__(player)
        self.model = Genetic(player)

    def next_move(self, game, print_board = False):
        mov = self.model.predict(game)
        game.add_piece(self.get_player(), mov)

        return mov

    def replay(self, winner):
        if winner == self.get_player():
            score = 100
        elif winner == 0:
            score = 0
        else:
            score = -100

        self.model.update(score)
        self.model.save_dataset()

def train_play(p1,p2,print_board = False):
    game = Gomoku()
    
    while True:
        _ = p1.next_move(game, print_board)
        if game.is_over()[0]:
            break

        _ = p2.next_move(game, print_board)
        if game.is_over()[0]:
            break

    winner = game.is_over()[1]
    return winner

def train(episodes):
    for e in range(episodes):
        p1 = GomukuGeneticAgent(1)
        p2 = GomukuGeneticAgent(-1)

        winner = train_play(p1,p2)
        p1.replay(winner)
        p2.replay(winner)

        p1 = GomukuGeneticAgent(1)
        p2 = GomukuGeneticAgent(-1)

        winner = train_play(p1,p2)
        p1.replay(winner)
        p2.replay(winner)

        p1 = GomukuGeneticAgent(1)
        p2 = GomukuAgent(-1)

        winner = train_play(p1,p2)
        p1.replay(winner)

        p1 = GomukuAgent(1)
        p2 = GomukuGeneticAgent(-1)

        winner = train_play(p1,p2)
        p2.replay(winner)

        print("Iternation : {}#".format(e))

def test():
    p1 = GomukuGeneticAgent(1)
    p2 = GomukuGeneticAgent(-1)

    winner = train_play(p1,p2, print_board = True)

if __name__ == "__main__":
    train(10000)
    test()






        