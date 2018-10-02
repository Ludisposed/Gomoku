# -*- coding: utf-8 -*-
import socket
import json
import random
import threading
import argparse
import re


class GomokuServer():
    def __init__(self, host, port, board_row, board_column):
        self.board_row = board_row
        self.board_column = board_column
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(2)
        print(f"Listing {self.host}:{self.port}")
        connection = []
        
        while True:
            self.waiting_for_connections(connection)
            self.listen_2_clients(connection)

    def close(self):
        self.sock.close()

    def listen_2_clients(self, connection):
        self.response = {"grid":[[0 for _ in range(self.board_column)] for _ in range(server.board_row)], 
                         "player": 2,
                         "gameover": -1}
        while True:
            data_arr = json.dumps(self.response).encode("utf-8")
            connection[0].send(data_arr)
            connection[1].send(data_arr)

            player1, player2 = self.recieve_information(connection)

            if player1 is None:
                self.sock.close()
                break

            self.response = self.process_positions(player1, player2)
        

    def waiting_for_connections(self, connection):
        while len(connection)<2:
            conn, addr = self.sock.accept()
            conn.settimeout(60)
            connection.append(conn)
            print(conn)
            print(connection)

    def recieve_information(self, connection):
        connection_0_data = connection[0].recv(1024)
        if connection_0_data == b'':
            print("connection 0 is GONE")
            return None, None

        connection_1_data = connection[1].recv(1024)
        if connection_1_data == b'':
            print("connection 1 is GONE")
            return None, None
        player_1_info = json.loads(connection_0_data.decode("utf-8"))
        player_2_info = json.loads(connection_1_data.decode("utf-8"))

        return player_1_info, player_2_info

    def process_positions(self, player1, player2):
        if self.response["player"] != player1["player"]:
            grid = player1["grid"]
            player = player1["player"]
            x = player1["x"]
            y = player1["y"]
        else:
            grid = player2["grid"]
            player = player2["player"]
            x = player2["x"]
            y = player2["y"]
        if self._check_win(grid, [x, y], player):
            gameover = 1
        elif self._check_draw(grid):
            gameover = 0
        else:
            gameover = -1
        return {"grid":grid, "player":player, "gameover":gameover}

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
    parser.add_argument('-i','--ip', type=str, default="localhost", help='server host')
    parser.add_argument('-p','--port', type=int, default=9999, help='server port')
    parser.add_argument('-r','--row', type=int, default=5, help='board row length')
    parser.add_argument('-c','--column', type=int, default=5, help='board column length')
  
    args = parser.parse_args()


    ip_pattern = "((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:(?<!\.)|\.)){4}"
    ip = re.match(ip_pattern, args.ip)
    valid_ip = (ip and ip.group(0) == args.ip)

    if not (args.ip == "localhost" or valid_ip):
        print("[-] IPV4 host is not valid")
        sys.exit(1)
    return args

if __name__ == "__main__":
    args = parse_options()
    server = GomokuServer(args.ip, args.port, args.row, args.column)
    try:
        server()
    except KeyboardInterrupt:
        server.close()



