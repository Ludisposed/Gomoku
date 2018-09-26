# -*- coding: utf-8 -*-
import socket
import json


def process_positions(player1, player2):
    if player1["x"] >= 0:
        return update(player1)
    elif player2["x"] >= 0:
        return update(player2)


def update(info):
    grid = info["grid"]
    player = info["player"]
    position = [info["x"], info["y"]]
    if check_win(grid, position, player):
        return grid, position, player, player
    return grid, position, player, -1


def waiting_for_connections():
    while len(connection) < 2:
        conn, addr = serversocket.accept()
        connection.append(conn)
        print(conn)
        print(connection)

def recieve_information():
    player_1_info = json.loads(connection[0].recv(1024))
    player_2_info = json.loads(connection[1].recv(1024))

    return player_1_info, player_2_info

def check_win(grid, position, player):
    target = 1 if player else 2
    if grid[position[0]][position[1]] != target:
        return False
    directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
    for direction in directions:
        continue_chess = 0
        for i in range(2):
            p = position[:]
            while 0 <= p[0] < 15 and 0 <= p[1] < 15:
                if grid[p[0]][p[1]] == target:
                    continue_chess += 1
                else:
                    break
                p[0] += direction[i][0]
                p[1] += direction[i][1]
        if continue_chess >= 6:
            return True
    return False

if __name__ == "__main__":
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("localhost", 9999))
    serversocket.listen(2)
    connection = []
    grid = [[0 for _ in range(15)] for _ in range(15)]
    position = [-1,-1]
    player = -1
    winner = -1
    while True:
        waiting_for_connections()
        data = json.dumps({"grid":grid, "x":position[0], "y":position[1], "player":player, "winner":winner}).encode("utf-8")
        connection[0].send(data)
        connection[1].send(data)

        player1, player2 = recieve_information()

        grid, position, player, winner = process_positions(player1, player2)
