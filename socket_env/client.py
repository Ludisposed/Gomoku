# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import socket
import argparse
import re
import sys
import json

'''
sent current player new position to server
receive another player's position from server and update client

'''

def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='Gomoku socket client @Ludisposed & @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python client.py -h '0.0.0.0' -p 9999
'''
                                        )
    parser.add_argument('-o','--host', type=str, default="localhost", help='server host')
    parser.add_argument('-p','--port', type=int, default=9999, help='server port')
    args = parser.parse_args()


    host_pattern = "((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:(?<!\.)|\.)){4}"
    host = re.match(host_pattern, args.host)
    valid_host = (host and host.group(0) == args.host)

    if not (args.host == "localhost" or valid_host):
        print("[-] IPV4 host is not valid")
        sys.exit(1)
    return args

def singleton(cls):
    instances = {}
    def _singleton(*args, **kwags):
        if cls not in instances:
            instances[cls] = cls(*args, **kwags)
        return instances[cls]
    return _singleton

@singleton
class GomokuClient(object):
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host,port))

    def send_data(self, player, x, y):
        data = {"player":player, "x":x, "y":y}
        self.client.send(json.dumps(data).encode("utf-8"))
    
    def receive_data(self):
        response = self.client.recv(4096)
        return json.loads(response.decode("utf-8"))

    def close(self):
        self.client.close()

def main(host, port):
    client = Client(host, port)

    try:
        client.send_data(1,0,0)
        print(client.receive_data())
    except KeyboardInterrupt:
        print("Failed")
        client.close_connection()

if __name__ == "__main__":
    args = parse_options()
    main(args.host,args.port) 
