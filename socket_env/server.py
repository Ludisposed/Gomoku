# -*- coding: utf-8 -*-
#!/usr/bin/env python3
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
# TODO: sent to target client
class GomokuTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                if not self.data:
                    break
                print(f"{self.client_address[0]}:{self.client_address[1]} wrote: {self.data}")
                response = json.dumps({"state":"ok"})
                self.request.sendall(response.encode("utf-8"))
            except:
                break

def main(ip, port):
    server = socketserver.TCPServer((ip, port), GomokuTCPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    args = parse_options()
    main(args.ip, args.port)
