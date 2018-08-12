import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)

def handle_client(client_socket):
    # print what client says
    request = client_socket.recv(1024)

    print "[*] Recieved %s" % request

    if(request=="new game"):
        client_socket.send("let's start a new game")
    # send back a packet
    client_socket.send("\n\nOK!")

    client_socket.close()

while True:
    try:
        client, addr = server.accept()

        print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])

        # spin the client thread to handle incoming data
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()
    except KeyboardInterrupt:
        server.close()
