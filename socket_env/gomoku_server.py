# -*- coding: utf-8 -*-
import socket
import json
import struct


def process_positions(data, player1, player2):
    if player1["x"] >= 0:
        return update(player1)
    elif player2["x"] >= 0:
        return update(player2)
    return data

def update(info):
    grid = info["grid"]
    player = info["player"]
    position = [info["x"], info["y"]]
    if check_win(grid, position, player):
        return grid, position, player, player
    return grid, position, player, -1

def waiting_for_connections(serversocket):
    connection = []
    while len(connection) < 2:
        conn, addr = serversocket.accept()
        connection.append(conn)
        print(conn)
        print(connection)
    return connection

def recieve_information(connection):
    connection_0_header_data = recv_n_bytes(connection[0], 4)
    connection_0_len = struct.unpack('<L', connection_0_header_data)[0]
    player_1_info = json.loads(recv_n_bytes(connection[0], connection_0_len).decode("utf-8"))
    
    connection_1_header_data = recv_n_bytes(connection[1], 4)
    connection_1_len = struct.unpack('<L', connection_1_header_data)[0]
    player_2_info = json.loads(recv_n_bytes(connection[1], connection_1_len).decode("utf-8"))

    return player_1_info, player_2_info

def recv_n_bytes(socket, n):
    data = b''
    while len(data) < n:
        chunk = socket.recv(n - len(data))
        if chunk == b'':
            break
        data += chunk
    return data

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

def main(ip, port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serversocket.bind((ip, port))
        serversocket.listen(2)
        grid = [[0 for _ in range(15)] for _ in range(15)]
        position = [-1,-1]
        player = -1
        winner = -1
        while True:
            connection = waiting_for_connections(serversocket)
            data = json.dumps({"grid":grid, "x":position[0], "y":position[1], "player":player, "winner":winner}).encode("utf-8")
            header = struct.pack('<L', len(data))
            connection[0].send(header+data)
            connection[1].send(header+data)

            player1, player2 = recieve_information(connection)
            print(player1)
            print(player2)

            grid, position, player, winner = process_positions((grid, position, player, winner), player1, player2)
    except KeyboardInterrupt:
        serversocket.close()

if __name__ == "__main__":
    main("localhost", 9999)










    
