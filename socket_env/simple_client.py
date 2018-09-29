import socket
import json
import sys
from random import choice

BOARD_ROW = 5
BOARD_COLUMN = 5

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("localhost", 50003))

def recieve_data():
    data = clientsocket.recv(1024).decode("utf-8")
    data = json.loads(data)

    return data

def random_move(grid):
    return choice([[i,j] for i in range(BOARD_ROW) for j in range(BOARD_COLUMN) if grid[i][j] == 0])

def print_grid(grid):
    print("\n".join([" | ".join(list(map(str, grid[i]))) for i in range(BOARD_ROW)]))

def next_move(grid, player):
    while True:
        position = input(f"What's your next move, separate by ',', only integer between 0-{BOARD_ROW} allowed:")
        x, y = position.split(",")
        try:
            x = int(x)
            y = int(y)
            if grid[x][y] == 0:
                grid[x][y] = player
                break
            print(f"Already has piece on {x}/{y}")
        except:
            pass
    return grid, x, y

# TODO: Fix First Move 
def display(player):
    
    while True:
        info = recieve_data()
        gameover = info["gameover"]
        last_player = info["player"]
        if gameover == -1:
            if last_player == player:
                clientsocket.send(json.dumps(info).encode("utf-8"))
            else:
                grid = info["grid"]
                print_grid(grid)
                grid, x, y = next_move(grid, player)
                print_grid(grid)
                print("Waiting...")
                data = {"grid":grid, "x":x, "y":y, "player":player}
                clientsocket.send(json.dumps(data).encode("utf-8"))
        else:
            if gameover == 0:
                print("Draw")
            else:
                if last_player == player:
                    print("You Win")
                else:
                    print("You Lost")
            clientsocket.close()
            break
       
if __name__ == "__main__":
    display(sys.argv[1])