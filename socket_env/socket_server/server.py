# -*- coding: utf-8 -*-
import json
import logging
import sys
import socketserver
import time
from settings import board_size
from handler import GomokuGameHandler

class GomokuRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('GomokuRequestHandler')
        self.logger.debug('__init__')
        self.logger.info(f"Client address: {client_address}")
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        self.logger.debug(f'handle: {self.client_address}')
        gomokuhandler = GomokuGameHandler(self.request)

        while True:
            try:
                connection_idx = self.server.connection_map.get(self.request)
                if connection_idx is None:
                    time.sleep(1)
                    continue
                connection = self.server.connections[connection_idx]
                
                if connection["connections"][connection["player"]] == self.request:
                    data = json.loads(self.request.recv(1024).decode("utf-8"))
                    self.logger.info(f"Receive from {self.client_address}: {data}")
                    gomokuhandler.handle(data, connection)
                else:
                    while True:
                        time.sleep(1)
                        connection = self.server.connections[connection_idx]
                        if connection["connections"][connection["player"]] == self.request:
                            x, y = connection["move"]
                            if connection["gameover"] >= 0:
                                self.request.send(json.dumps({"x":x, "y":y ,"gameover": -1 * connection["gameover"]}).encode('utf-8'))
                            else:
                                self.request.send(json.dumps({"x":x, "y":y, "gameover": -2}).encode('utf-8'))
                            break
            except Exception as e:
                self.logger.error(e)
                break

    def finish(self):
        self.logger.debug(f'finish: {self.client_address}')
        return socketserver.BaseRequestHandler.finish(self)

    

class GomokuServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, handle_class=GomokuRequestHandler):
        print(board_size)
        self.logger = logging.getLogger('GomokuServer')
        self.logger.debug('__init__')
        self.connections = []
        self.waiting = []
        self.connection_map = {}
        super(GomokuServer, self).__init__(server_address, handle_class)

    def serve_forever(self, poll_interval=0.5):
        self.logger.info('Handling requests, press <Ctrl-C> to quit')
        super(GomokuServer, self).serve_forever(poll_interval)

    def handle_request(self):
        self.logger.debug('handle_request')
        return super(GomokuServer, self).handle_request()

    def process_request(self, request, client_address):
        self.logger.debug('process_request')
        self.add_connection(request)
        return super(GomokuServer, self).process_request(request, client_address)

    def close_request(self, request_address):
        self.logger.debug(f'close_request({request_address})')
        super(GomokuServer, self).close_request(request_address)

    def add_connection(self, request):
        if len(self.waiting) == 0:
            self.waiting.append(request)
        elif len(self.waiting) == 1:
            self.waiting += [request]
            idx = len(self.connections)
            self.connections += [{"connections":self.waiting, "grid":"0"*(board_size[0]*board_size[1]), "player":0, "gameover":-1, "move":(-1,-1)}]

            for i in range(len(self.waiting)):
                sock = self.waiting[i]
                self.connection_map[sock] = idx
                data = {"player":i+1, "row":board_size[0], "column":board_size[1]}
                data = json.dumps(data).encode("utf-8")
                sock.send(data)
            self.waiting = []

    def _remove_connections(self, connections, idx):
        for conn in connections:
            conn.close()
            del self.connection_map[conn]
        del self.connections[idx]

