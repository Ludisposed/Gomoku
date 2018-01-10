from gomoku_game import Gomoku
from gomoku_agent import GomokuGeneticAgent, GomokuRandomAgent

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

        p1 = GomokuGeneticAgent(1)
        p2 = GomokuRandomAgent(-1)

        winner = train_play(p1,p2)
        p1.replay(winner)

        p1 = GomokuRandomAgent(1)
        p2 = GomokuGeneticAgent(-1)

        winner = train_play(p1,p2)
        p2.replay(winner)

        p1 = GomokuGeneticAgent(1)
        p2 = GomokuGeneticAgent(-1)

        winner = train_play(p1,p2)
        p1.replay(winner)
        p2.replay(winner)

        print("Iternation : {}#".format(e))

def test():
    p1 = GomokuGeneticAgent(1)
    p2 = GomokuGeneticAgent(-1)

    return train_play(p1,p2, print_board = True)

if __name__ == "__main__":
    #train(10000)
    print(test())






        