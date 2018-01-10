from numpy import random, sqrt, exp, dot, argmax
from random import choices, choice, uniform
import pickle
import os

class Genome():
    def __init__(self, three_mine_pieces_in_open_row       = uniform(0, 1),
                       three_opponent_pieces_in_open_row   = uniform(0, 1),
                       two_mine_pieces_in_open_row         = uniform(0, 1),
                       two_opponent_pieces_in_open_row     = uniform(0, 1),
                       four_mine_pieces_in_open_row        = uniform(0, 1),
                       four_opponent_pieces_in_open_row    = uniform(0, 1),
                       five_mine_pieces_in_row             = uniform(0, 1),
                       five_opponent_pieces_in_row         = uniform(0, 1),
                       fitness                             = -1):
        self.two_mine_pieces_in_open_row         = two_mine_pieces_in_open_row
        self.two_opponent_pieces_in_open_row     = two_opponent_pieces_in_open_row
        self.three_mine_pieces_in_open_row       = three_mine_pieces_in_open_row
        self.three_opponent_pieces_in_open_row   = three_opponent_pieces_in_open_row
        self.four_mine_pieces_in_open_row        = four_mine_pieces_in_open_row
        self.four_opponent_pieces_in_open_row    = four_opponent_pieces_in_open_row
        self.five_mine_pieces_in_row             = five_mine_pieces_in_row
        self.five_opponent_pieces_in_row         = five_opponent_pieces_in_row
        self.fitness                             = fitness

#train 10 games test 1 games to get fitness for that genomes
class Genetic:
    def __init__(self):
        self.mutation_rate = 0.2
        self.mutation_step = 0.2

        self.current_genome = -1
        self.population_size = 10
        self.genomes = []
        self.read_dataset()
        self.evaluate_next_genome()

    def update(self, score):
        self.genomes[self.current_genome].fitness = score
        self.evaluate_next_genome()

    def predict(self, game, player):
        board = game.get_board()
        current_moves = self.predict_one_depth(board, player)
        current_player = player
        #depth = 6
        #soooo slow
        for i in range(5):
            print("In depth {}#".format(i+1))
            current_player *= (-1)
            for move in current_moves:
                next_board = move[3]
                next_moves = self.predict_one_depth(next_board, current_player)
                next_best_move = self.best_choice(next_moves)
                if current_player == player:
                    move[1] += next_best_move[1]
                    move[2] += next_best_move[2]
                else:
                    move[2] += next_best_move[1]
                    move[1] += next_best_move[2]
                move[3][next_best_move[0]] = current_player
        return self.best_choice(current_moves)[0]

    def best_choice(self, scores):
        return max(scores, key = lambda x: 0.5 * x[1] + (-0.5) * x[2])

    def predict_one_depth(self, board, player):
        valid_choices = [idx for idx in range(len(board)) if board[idx] == 0]
        scores = []
        for pos in valid_choices:
            new_board = board[:]
            new_board[pos] = player
            scores += [[pos, self.score(new_board, player), self.score(new_board, player * (-1)) ,new_board]]
        return scores

    def score(self, board, player):
        targets = [0 for _ in range(8)]

        for i in range(15):
            for j in range(15):
                for n in [1,14,15,16]:
                    for m in range(2,6):

                        pieces_in_one_line = (i * 15 + j + (m-1) * n) // 15 == ((i * 15 + j) // 15) + ((m-1) if n > 1 else 0)

                        open_line = i * 15 + j - n >= 0 and board[i * 15 + j - n] == 0 and\
                                    i * 15 + j + m * n < 225 and board[i * 15 + j + m * n] == 0

                        same_piece_in_line = i * 15 + j + (m-1) * n < 225 and len(set([board[i * 15 + j + k * n] for k in range(m)])) == 1
        
                        if board[i * 15 + j] !=0 and \
                           pieces_in_one_line and \
                           (open_line if m < 5 else True) and \
                           same_piece_in_line:
                            
                            if board[i * 15 + j] == player:
                                targets[(m - 2) * 2] += 1
                            else:
                                targets[(m - 2) * 2 + 1] += 1
                    


        return targets[0] * self.genomes[self.current_genome].two_mine_pieces_in_open_row +\
               targets[1] * self.genomes[self.current_genome].two_opponent_pieces_in_open_row +\
               targets[2] * self.genomes[self.current_genome].three_mine_pieces_in_open_row +\
               targets[3] * self.genomes[self.current_genome].three_opponent_pieces_in_open_row +\
               targets[4] * self.genomes[self.current_genome].four_mine_pieces_in_open_row +\
               targets[5] * self.genomes[self.current_genome].four_opponent_pieces_in_open_row +\
               targets[6] * self.genomes[self.current_genome].five_mine_pieces_in_row +\
               targets[7] * self.genomes[self.current_genome].five_opponent_pieces_in_row


        

    def evaluate_next_genome(self):
        self.current_genome += 1
        if self.current_genome >= self.population_size:
            self.evolve()

    def evolve(self):
        self.current_genome = 0
        self.genomes = sorted(self.genomes, key = lambda x: -x.fitness)
        while len(self.genomes) > self.population_size // 2:
            self.genomes.pop()
        children = [self.genomes[0]]
        while len(children) < self.population_size:
            children += [self.make_child(choices(self.genomes, k=2))]
        self.genomes = children

    def make_child(self, parents):
        mum, dad = parents
        
        child = Genome(two_mine_pieces_in_open_row         = choice([mum.two_mine_pieces_in_open_row,         dad.two_mine_pieces_in_open_row]),
                       two_opponent_pieces_in_open_row     = choice([mum.two_opponent_pieces_in_open_row,     dad.two_opponent_pieces_in_open_row]),
                       three_mine_pieces_in_open_row       = choice([mum.three_mine_pieces_in_open_row,       dad.three_mine_pieces_in_open_row]),
                       three_opponent_pieces_in_open_row   = choice([mum.three_opponent_pieces_in_open_row,   dad.three_opponent_pieces_in_open_row]),
                       four_mine_pieces_in_open_row        = choice([mum.four_mine_pieces_in_open_row,        dad.four_mine_pieces_in_open_row]),
                       four_opponent_pieces_in_open_row    = choice([mum.four_opponent_pieces_in_open_row,    dad.four_opponent_pieces_in_open_row]),
                       five_mine_pieces_in_row             = choice([mum.five_mine_pieces_in_row,             dad.five_mine_pieces_in_row]),
                       five_opponent_pieces_in_row         = choice([mum.five_opponent_pieces_in_row,         dad.five_opponent_pieces_in_row]))
        if uniform(0, 1) < self.mutation_rate:
            child.two_mine_pieces_in_open_row         += uniform(0, 1) * self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.two_opponent_pieces_in_open_row      += uniform(0, 1) * self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.three_mine_pieces_in_open_row       += uniform(0, 1) * self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.three_opponent_pieces_in_open_row   += uniform(0, 1) * self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.four_mine_pieces_in_open_row        += uniform(0, 1) * self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.four_opponent_pieces_in_open_row    += uniform(0, 1) * self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.five_mine_pieces_in_row             += uniform(0, 1) * self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.five_opponent_pieces_in_row         += uniform(0, 1) * self.mutation_step * 2 - self.mutation_step
        
        return child

    def save_dataset(self):
        with open('genomes', 'wb+') as f:
            pickle.dump((self.genomes, self.current_genome), f, -1)
    def read_dataset(self):
        if not os.path.isfile('genomes'):
            self.genomes = [Genome() for _ in range(self.population_size)]
            
        else:
            with open('genomes', 'rb') as f:
                self.genomes, self.current_genome = pickle.load(f)
