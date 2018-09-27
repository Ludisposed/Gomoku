# -*- coding: utf-8 -*-
import json
import queue
import argparse
import re
from random import choice

from socketclientthread import SocketClientThread, ClientCommand, ClientReply


def creat_client():
    clientsocket = SocketClientThread()
    clientsocket.start()
    
    return clientsocket

def send_data(clientsocket, data):
    print(f"[*] send data:{data}")
    clientsocket.cmd_q.put(ClientCommand(ClientCommand.SEND, data))
    print(list(clientsocket.cmd_q.queue)[0])
    reply = clientsocket.reply_q.get(True)
    print(reply.type_, reply.data)
    
def on_client_reply_timer(clientsocket, server_addr, player):
    while True:
        clientsocket.cmd_q.put(ClientCommand(ClientCommand.CONNECT, server_addr))
        clientsocket.cmd_q.put(ClientCommand(ClientCommand.RECEIVE))
        try:
            reply = clientsocket.reply_q.get(block=True)
            print(reply.type_, reply.data)
            if reply.data == "Socket closed prematurely":
                close_connection(clientsocket)
                break
            if reply.type_ == ClientReply.SUCCESS and reply.data is not None:
                print("[+] ready for next package")
                if next_pacakge(clientsocket, reply.data, player) == 0:
                    clientsocket.cmd_q.put(ClientCommand(ClientCommand.CLOSE))
                    break
        except queue.Empty:
            pass
        clientsocket.cmd_q.put(ClientCommand(ClientCommand.CLOSE))

def close_connection(clientsocket):
    clientsocket.cmd_q.put(ClientCommand(ClientCommand.CLOSE))


def parse(data):
    data = json.loads(data.decode("utf-8"))
    return data["grid"], data["player"], data["winner"]

def random_move(grid):
    return choice([[i,j] for i in range(15) for j in range(15) if grid[i][j] == 0])

def next_pacakge(clientsocket, data, player):
    grid, last_player, winner = parse(data)
    print(f"Parsed Data: \nGrid:{grid}\nLast_Player:{last_player}\nWinner:{winner}")
    if winner > 0:
        print(f"[+] Game Over Winner is player No.:{last_player}")
        return 0
    elif winner == 0:
        print("[+] Game Over Draw")
        return 0
    else:
        if last_player != player:
            print(f"[*] Now is for Player No.{player}")
            x, y = random_move(grid)
            print(f"[*] Next Random Move {x}/{y}")
            grid[x][y] = player
            data = {"grid":grid, "x":x, "y":y, "player":player}
            print(f"[*] Data to be send to server: {data}")
            send_data(clientsocket, json.dumps(data).encode("utf-8"))
        else:
            print(f"[*] NOT MY TURN FROM Player No.{player}")
            data = {"grid":[], "x":-1, "y":-1, "player":player}
            print(f"[*] Data to be send to server: {data}")
            send_data(clientsocket, json.dumps(data).encode("utf-8"))
    return 1

def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='Gomoku socket client test @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python socket_test.py -h '0.0.0.0' -p 9999 -e 1
'''
                                        )
    parser.add_argument('-o','--host', type=str, default="localhost", help='server host')
    parser.add_argument('-p','--port', type=int, default=9999, help='server port')
    parser.add_argument('-e','--player', type=int, default=1, help='player')
    args = parser.parse_args()


    host_pattern = "((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:(?<!\.)|\.)){4}"
    host = re.match(host_pattern, args.host)
    valid_host = (host and host.group(0) == args.host)

    if not (args.host == "localhost" or valid_host):
        print("[-] IPV4 host is not valid")
        sys.exit(1)
    return args

if __name__ == "__main__":
    args = parse_options()
    clientsocket = creat_client()
    on_client_reply_timer(clientsocket, (args.host, args.port), args.player)

        

