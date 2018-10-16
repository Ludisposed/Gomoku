# -*- coding: utf-8 -*-
import socket
import json
import random
import threading
import argparse
import re

'''
TODO: 
1. focus on multithread
2. add GUI to client game

Update Process:
1. First step, send board_row and board_column to client
2. A server can handle lots(one-one) game, not just two player
3. MiMT attack

'''
class GomokuServer():
    def __init__(self, port, board_row, board_column):
        self.board_row = board_row
        self.board_column = board_column
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("localhost", self.port))
        self.connections = []
        self.waiting = []
        self.connection_map = {}

    def listen(self):
        self.sock.listen(2)
        print(f"Listing localhost:{self.port}")
        
        while True:
            client_socket, addr = self.sock.accept()
            print(f"Connection from {addr[0]}:{addr[1]}")
            self.add_connection(client_socket)
            client_socket.settimeout(60)

    def close(self):
        self.sock.close()

    def add_connection(self, client_socket):
        if len(self.waiting) == 0:
            self.waiting.append(client_socket)
        elif len(self.waiting) == 1:
            self.waiting += [client_socket]
            idx = len(self.connections)
            self.connections += [{"connections":self.waiting, "grid":"0"*(self.board_row*self.board_column), "player":0}]

            for i in range(len(self.waiting)):
                sock = self.waiting[i]
                self.connection_map[sock] = idx
                data = {"player":i+1, "row":self.board_row, "column":self.board_column}
                data = json.dumps(data).encode("utf-8")
                sock.send(data)
                client_thread = threading.Thread(target=self.handle_client, args=(sock,))
                client_thread.start()
            self.waiting = []

    def handle_client(self, client_socket):
        print(f"Client: {client_socket}")
        connection_idx = self.connection_map.get(client_socket)
        print(connection_idx)
        if connection_idx is not None:
            connection = self.connections[connection_idx]
            data = json.loads(client_socket.recv(1024).decode("utf-8"))
            print(f"Receive from {client_socket}: {data}")
            if connection["connections"][connection["player"]] == client_socket:
                
                grid, gameover = self._update_grid(connection["grid"], data, connection["player"]+1)
                if gameover >= 0:
                    for conn in connection["connections"]:
                        conn.sent(json.dumps({"gameover":gameover*(1 if conn == client_socket else -1)}).encode('utf-8'))
                    # self._remove_connections(connection["connections"])
                else:
                    next_player = connection["player"] ^ 1
                    next_player_socket = connection["connections"][next_player]
                    data["gameover"] = -2
                    next_player_socket.send(json.dumps(data).encode('utf-8'))
                    connection["player"] = next_player
                    connection["grid"] = grid


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

    def _remove_connections(self, connections, idx):
        for conn in connections:
            conn.close()
            del self.connection_map[conn]
        del self.connections[idx]

    def grid_str_2_matrix(self, grid):
        
        return [list(map(int, grid[i:i+self.board_column])) for i in range(0, len(grid), self.board_column)]

    def grid_matrix_2_str(self, grid):
        return "".join("".join(str(grid[i][j]) for j in range(self.board_column)) for i in range(self.board_row))

    def _check_draw(self, grid):
        return all([grid[i][j] != 0 for i in range(self.board_row) for j in range(self.board_column)])

    def _check_win(self, grid, position, player):
        target = player
        if grid[position[0]][position[1]] != target:
            return False
        directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
        for direction in directions:
            continue_chess = 0
            for i in range(2):
                p = position[:]
                while 0 <= p[0] < self.board_row and 0 <= p[1] < self.board_column:
                    if grid[p[0]][p[1]] == target:
                        continue_chess += 1
                    else:
                        break
                    p[0] += direction[i][0]
                    p[1] += direction[i][1]

            if continue_chess >= 6:
                return True
        return False

    def __call__(self):
        return self.listen()

def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='Gomoku socket server @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python server.py -i '0.0.0.0' -p 9999
'''
                                        )
    parser.add_argument('-p','--port', type=int, default=9999, help='server port')
    parser.add_argument('-r','--row', type=int, default=5, help='board row length')
    parser.add_argument('-c','--column', type=int, default=5, help='board column length')
  
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_options()
    server = GomokuServer(args.port, args.row, args.column)
    try:
        server()
    except KeyboardInterrupt:
        server.close()



