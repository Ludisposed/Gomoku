# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import socket
import threading
import socketserver
import argparse
import re
import sys
import json

'''
version 1: only two players connect to this server
receive position json data from one client and sent it anther client
'''

def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='Gomoku socket server @Ludisposed & @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python server.py -i '0.0.0.0' -p 9999
'''
                                        )
    parser.add_argument('-i','--ip', type=str, default="0.0.0.0", help='server host')
    parser.add_argument('-p','--port', type=int, default=9999, help='server port')
    args = parser.parse_args()


    ip_pattern = "((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:(?<!\.)|\.)){4}"
    ip = re.match(ip_pattern, args.ip)
    valid_ip = (ip and ip.group(0) == args.ip)

    if not (args.ip == "localhost" or valid_ip):
        print("[-] IPV4 host is not valid")
        sys.exit(1)
    return args


client_addr = []
client_socket = []

# socketserver is good also might can consider websocket
class GomokuTCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        ip = self.client_address[0].strip()
        port = self.client_address[1]
        print(f"{ip}:{port} is connect!")
        client_addr.append(self.client_address)
        client_socket.append(self.request)

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]}:{self.client_address[1]} wrote: {self.data}")
        response = json.dumps({"state":"ok"})
        self.request.sendall(response.encode("utf-8"))

    def finish(self):
        ip = self.client_address[0].strip()
        port = self.client_address[1]
        print(f"{ip}:{port} is disconnect!")
        client_addr.remove(self.client_address)
        client_socket.remove(self.request)

class GomokuTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

def main(ip, port):
    server = GomokuTCPServer((ip, port), GomokuTCPRequestHandler)
    host, p = server.server_address
    print(host, p)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    client("localhost", p)
    client("localhost", p)

    for s in client_socket:
        s.sendall(b"hello")

    server.shutdown()
    server.server_close()

if __name__ == "__main__":
    args = parse_options()
    main(args.ip, args.port)
