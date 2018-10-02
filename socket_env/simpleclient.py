import socket
import json
import sys
import argparse
import re
import threading
import queue

def singleton(cls):
    instances = {}
    def _singleton(*args, **kwags):
        if cls not in instances:
            instances[cls] = cls(*args, **kwags)
        return instances[cls]
    return _singleton

@singleton
class GomokuClient():
    def __init__(self):
        self._client = None

    @property
    def client(self):
        return self._client
    
    def connect(self, host, port):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect((host, port))

    def send(self, data):
        self._client.send(json.dumps(data).encode("utf-8"))
    
    def receive(self):
        response = self._client.recv(4096)
        return json.loads(response.decode("utf-8"))

    def close(self):
        self._client.close()
        self._client = None

class ClientCommand():
    CONNECT, SEND, RECEIVE, CLOSE = range(4)
    def __init__(self, type_, data=None):
        self.type_ = type_
        self.data = data


class GomokuClientThread(threading.Thread):
    def __init__(self, send_q=queue.Queue(), reply_q=queue.Queue()):
        super(GomokuClientThread, self).__init__()
        self.cmd_q = send_q
        self.reply_q = reply_q
        self.clientsocket = GomokuClient()
        self.handlers = {
            ClientCommand.CONNECT: self.connect,
            ClientCommand.CLOSE: self.close,
            ClientCommand.SEND: self.send,
            ClientCommand.RECEIVE: self.recieve,
        }
    
    def run(self):
        while True:
            try:
                cmd = self.cmd_q.get(True, 0.1)
                self.handlers[cmd.type_](cmd.data)
            except queue.Empty as e:
                continue

    def connect(self, data):
        host, port = data
        self.clientsocket.connect(host, port)
        self.cmd_q.put(ClientCommand(ClientCommand.RECEIVE))

    def send(self, data):
        if data.get("grid"):
            data["grid"] = self.grid_matrix_2_str(data["grid"])
        self.clientsocket.send(data)
        self.cmd_q.put(ClientCommand(ClientCommand.RECEIVE))

    def recieve(self, data=None):
        data = self.clientsocket.receive()
        if data:
            self.reply_q.put(data)

    def close(self, data=None):
        self.clientsocket.close()
    
    def grid_matrix_2_str(self, grid):
        n = len(grid)
        m = len(grid[0])
        return "".join("".join(str(grid[i][j]) for j in range(m)) for i in range(n))
    

class GomokuGame():
    def __init__(self, player, board_row=5, board_column=5, host="localhost", port=50003):
        self.board_row = board_row
        self.board_column = board_column
        self.player = player
        self.host = host
        self.port = port

    def display(self):
        client_thread = GomokuClientThread()
        client_thread.start()
        client_thread.cmd_q.put(ClientCommand(ClientCommand.CONNECT, (self.host, self.port)))
        while True:
            data = client_thread.reply_q.get(True)
            grid = self.grid_str_2_matrix(data["grid"])
            if data["gameover"] == -1:
                if data["next_player"] != self.player:
                    client_thread.cmd_q.put(ClientCommand(ClientCommand.SEND, {"wait": True}))
                else:
                    self.print_grid(grid)
                    grid, x, y = self.next_move(grid)
                    self.print_grid(grid)
                    print("Waiting...")
                    data = {"grid":grid, "x":x, "y":y, "player":self.player}
                    client_thread.cmd_q.put(ClientCommand(ClientCommand.SEND, data))
            else:
                if data["gameover"] == 0:
                    print("Draw")
                else:
                    if data["player"] == self.player:
                        print("You Win")
                    else:
                        print("You Lost")
                client_thread.cmd_q.put(ClientCommand(ClientCommand.CLOSE))
                break

    def grid_str_2_matrix(self, grid):
        return [list(map(int, grid[i:i+self.board_column])) for i in range(0, len(grid), self.board_column)]

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
    game = GomokuGame(args.player, host=args.ip, port=args.port)
    game()