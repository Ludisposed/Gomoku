import socket
import threading
import argparse
import re
import sys

def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='Gomoku socket server @Ludisposed & @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python client.py -h '0.0.0.0' -p 9999
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

def handle_client(client_socket):
    # print what client says
    request = client_socket.recv(1024)

    print(f"[*] Recieved: {request.decode('utf-8')}")

    if(request=="new game"):
        client_socket.send("let's start a new game")
    # send back a packet
    client_socket.send(b"\n\nOK!")

    client_socket.close()

def main(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f"[*] Listening on {ip}:{port}")

    while True:
        try:
            client, addr = server.accept()

            print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")

            # spin the client thread to handle incoming data
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()
        except KeyboardInterrupt:
            server.close()

if __name__ == "__main__":
    args = parse_options()
    main(args.ip, args.port)
