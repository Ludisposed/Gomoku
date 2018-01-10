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
                for n in [1,14,15,16]:

                    pieces_in_one_line = (i * 15 + j + 4 * n) // 15 == ((i * 15 + j) // 15) + (4 if n > 1 else 0)
                    same_piece_in_line = i * 15 + j + 4 * n < 225 and len(set([board[i * 15 + j + k * n] for k in range(5)])) == 1

                    if board[i * 15 + j] != 0 and \
                       pieces_in_one_line and \
                       same_piece_in_line:
                        
                        return True, board[i * 15 + j]
        if len(self.get_empty_pos()) == 0:
            return True, 0
        return False, 0

    def __str__(self):
        board = ['X' if x == 1 else x for x in self.board]
        board = ['O' if x == -1 else x for x in board]
        board = ['.' if x == 0 else x for x in board]
        return '\n'.join(' | '.join(board[i * 15 + j] for j in range(15)) for i in range(15))
