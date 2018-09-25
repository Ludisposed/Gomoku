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

def main(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host,port))

    while True:
        # Send
        sendstring = input("What do we want to send>>> ")
        client.send(sendstring.encode("utf-8"))
        # Recieve
        response = client.recv(4096)
        print(response.decode("utf-8"))

if __name__ == "__main__":
    args = parse_options()
    main(args.host,args.port) 
