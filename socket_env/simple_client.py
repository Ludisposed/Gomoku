import socket
import json
import sys
from random import choice

BOARD_ROW = 5
BOARD_COLUMN = 5

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("0.0.0.0", 50003))

def recieve_data():
    data = clientsocket.recv(1024).decode("utf-8")
    data = json.loads(data)

    return data

def random_move(grid):
    return choice([[i,j] for i in range(BOARD_ROW) for j in range(BOARD_COLUMN) if grid[i][j] == 0])


def display(player):
    
    while True:
        info = recieve_data()
        gameover = info["gameover"]
        if not gameover:
            if info["player"] == player:
                clientsocket.send(json.dumps(info).encode("utf-8"))
            else:
                grid = info["grid"]
                x, y = random_move(grid)
                grid[x][y] = player
                data = {"grid":grid, "player":player}
                clientsocket.send(json.dumps(data).encode("utf-8"))
        else:
            clientsocket.close()
            break
       
if __name__ == "__main__":
    display(sys.argv[1])