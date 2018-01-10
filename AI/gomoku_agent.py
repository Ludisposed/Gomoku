import abc
from genetic import Genetic
from random import choice

#from keras.models import Model

class GomokuAgent():
    def __init__(self, player):
        self.player = player
        self.model = self.buildmodel()

    def get_player(self):
        return self.player

    @abc.abstractmethod
    def buildmodel(self):
        return None

    def next_move(self, game, print_board = False):
        mov = self.model.predict(game, self.get_player())
        game.add_piece(self.get_player(), mov)

        if print_board:
            print(game)

        return mov

class GomokuQLearningAgent(GomokuAgent):
    def buildmodel(self):
        pass


class GomokuGeneticAgent(GomokuAgent):
    def buildmodel(self):
        return Genetic()

    def replay(self, winner):
        if winner == self.get_player():
            score = 100
        elif winner == 0:
            score = 0
        else:
            score = -100

        self.model.update(score)
        self.model.save_dataset()

class GomokuRandomAgent(GomokuAgent):
    def buildmodel(self):
        return RandomModel()

class RandomModel():
    def predict(self, game, player):
        empty_positions = game.get_empty_pos()
        return choice(empty_positions)
