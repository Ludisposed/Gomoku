import socket
import json
import sys
import argparse
import re


class GomokuClient():
    def __init__(self, player, host="localhost", port=50003, board_row=5, board_column=5):
        self.host = host
        self.port = port
        self.board_row = board_row
        self.board_column = board_column
        self.player = player
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def display(self):
        while True:
            info = self.recieve_data()
            gameover = info["gameover"]
            last_player = info["player"]
            if gameover == -1:
                if last_player == self.player:
                    self.sock.send(json.dumps(info).encode("utf-8"))
                else:
                    grid = info["grid"]
                    self.print_grid(grid)
                    grid, x, y = self.next_move(grid)
                    self.print_grid(grid)
                    print("Waiting...")
                    data = {"grid":grid, "x":x, "y":y, "player":self.player}
                    self.sock.send(json.dumps(data).encode("utf-8"))
            else:
                if gameover == 0:
                    print("Draw")
                else:
                    if last_player == self.player:
                        print("You Win")
                    else:
                        print("You Lost")
                self.sock.close()
                break

    def recieve_data(self):
        data = self.sock.recv(1024).decode("utf-8")
        data = json.loads(data)
        return data

    def print_grid(self, grid):
        print("\n".join([" | ".join(list(map(str, grid[i]))) for i in range(self.board_row)]))

    def next_move(self, grid):
        while True:
            position = input(f"What's your next move, separate by ',', only integer between 0-{self.board_row} allowed:")
            x, y = position.split(",")
            try:
                x = int(x)
                y = int(y)
                if grid[x][y] == 0:
                    grid[x][y] = self.player
                    break
                print(f"Already has piece on {x}/{y}")
            except:
                pass
        return grid, x, y

    def __call__(self):
        return self.display()

def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='Gomoku socket client @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python server.py -i '0.0.0.0' -p 9999
'''
                                        )
    parser.add_argument('-i','--ip', type=str, default="localhost", help='server host')
    parser.add_argument('-p','--port', type=int, default=9999, help='server port')
    parser.add_argument('-e','--player', type=int, default=1, help='player')
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
    client = GomokuClient(args.player, args.ip, args.port)
    client()