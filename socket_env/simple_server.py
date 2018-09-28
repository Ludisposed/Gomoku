# -*- coding: utf-8 -*-
import socket, json, random

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("0.0.0.0", 50003))
serversocket.listen(2)
connection = []
BOARD_ROW = 5
BOARD_COLUMN = 5

def process_positions(arr, player1, player2):
    if arr["player"] != player1["player"]:
        grid = player1["grid"]
        player = player1["player"]
    else:
        grid = player2["grid"]
        player = player2["player"]
    gameover = grid_full(grid)
    return {"grid":grid, "player":player, "gameover":gameover}

def grid_full(grid):
    return all([grid[i][j] != 0 for i in range(BOARD_ROW) for j in range(BOARD_COLUMN)])

def waiting_for_connections():
    while len(connection)<2:
        conn, addr = serversocket.accept()
        connection.append(conn)
        print(conn)
        print(connection)

def recieve_information():
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

if __name__ == "__main__":
    try:
        grid = [[0 for _ in range(BOARD_COLUMN)] for _ in range(BOARD_ROW)]
        player = 2
        gameover = False
        arr = {"grid":grid, "player":player, "gameover":gameover}
        while True:
            waiting_for_connections()
            data_arr = json.dumps(arr).encode("utf-8")
            print(data_arr)
            connection[0].send(data_arr)
            connection[1].send(data_arr)

            player1, player2 = recieve_information()

            if player1 is None:
                serversocket.close()
                break

            arr = process_positions(arr, player1, player2)
    except KeyboardInterrupt:
        serversocket.close()
