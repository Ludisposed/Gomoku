# -*- coding: utf-8 -*-
import socket, json, random

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("localhost", 50003))
serversocket.listen(2)
connection = []
BOARD_ROW = 5
BOARD_COLUMN = 5

def process_positions(arr, player1, player2):
    if arr["player"] != player1["player"]:
        grid = player1["grid"]
        player = player1["player"]
        x = player1["x"]
        y = player1["y"]
    else:
        grid = player2["grid"]
        player = player2["player"]
        x = player2["x"]
        y = player2["y"]
    if check_win(grid, [x, y], player):
        gameover = 1
    elif check_draw(grid):
        gameover = 0
    else:
        gameover = -1
    return {"grid":grid, "player":player, "gameover":gameover}

def check_draw(grid):
    return all([grid[i][j] != 0 for i in range(BOARD_ROW) for j in range(BOARD_COLUMN)])

def check_win(grid, position, player):
    target = player
    if grid[position[0]][position[1]] != target:
        return False
    directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
    for direction in directions:
        continue_chess = 0
        for i in range(2):
            p = position[:]
            while 0 <= p[0] < BOARD_ROW and 0 <= p[1] < BOARD_COLUMN:
                if grid[p[0]][p[1]] == target:
                    continue_chess += 1
                else:
                    break
                p[0] += direction[i][0]
                p[1] += direction[i][1]

        if continue_chess >= 6:
            return True
    return False

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
        gameover = -1
        arr = {"grid":grid, "player":player, "gameover":gameover}
        while True:
            waiting_for_connections()

            data_arr = json.dumps(arr).encode("utf-8")
            connection[0].send(data_arr)
            connection[1].send(data_arr)

            player1, player2 = recieve_information()

            if player1 is None:
                serversocket.close()
                break

            arr = process_positions(arr, player1, player2)
    except KeyboardInterrupt:
        serversocket.close()
