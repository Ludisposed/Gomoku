# -*- coding: utf-8 -*-
from settings import board_size
import json

class GomokuGameHandler():
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def handle(self, data, connection):
        x,y = data.values()          
        grid, gameover = self._update_grid(connection["grid"], data, connection["player"]+1)
        connection["grid"] = grid
        connection["move"] = (data["x"], data["y"])
        connection["player"] ^= 1

        if gameover >= 0:            
            connection["gameover"] = connection["player"]+1 if gameover > 0 else 0
            self.client_socket.send(json.dumps({"x":x,"y":y,"gameover": gameover}).encode('utf-8'))


    def _update_grid(self, grid, move_data, player):
        grid = self.grid_str_2_matrix(grid)
        x, y = move_data.values()
        grid[x][y] = player
        gameover = -1
        if self._check_win(grid, [x, y], player):
            gameover = 1
        elif self._check_draw(grid):
            gameover = 0
        grid = self.grid_matrix_2_str(grid)
        return grid, gameover

    def grid_str_2_matrix(self, grid):
        
        return [list(map(int, grid[i:i+board_size[1]])) for i in range(0, len(grid), board_size[1])]

    def grid_matrix_2_str(self, grid):
        return "".join("".join(str(grid[i][j]) for j in range(board_size[1])) for i in range(board_size[0]))

    def _check_draw(self, grid):
        return all([grid[i][j] != 0 for i in range(board_size[0]) for j in range(board_size[1])])

    def _check_win(self, grid, position, player):
        target = player
        if grid[position[0]][position[1]] != target:
            return False
        directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
        for direction in directions:
            continue_chess = 0
            for i in range(2):
                p = position[:]
                while 0 <= p[0] < board_size[0] and 0 <= p[1] < board_size[1]:
                    if grid[p[0]][p[1]] == target:
                        continue_chess += 1
                    else:
                        break
                    p[0] += direction[i][0]
                    p[1] += direction[i][1]

            if continue_chess >= 6:
                return True
        return False