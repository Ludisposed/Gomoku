# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import socket
import argparse
import re
import sys
import json

#I like this singleton, need it later
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
        self.start(host, port)

    def start(self, host, port):
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
        self.client = None

def main(host, port):
    client = GomokuClient(host, port)

    try:
        while True:
            sendata = input("What you wanna send >> ")
            data = sendata.split(",")
            client.send_data(data[0],data[1],data[2])
            print(client.receive_data())
    except KeyboardInterrupt:
        print("Failed")
        client.close_connection()

if __name__ == "__main__":
    args = parse_options()
    main(args.host,args.port) 
