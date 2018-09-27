# -*- coding: utf-8 -*-
import socket
import struct
import threading
import queue
import json

class ClientCommand():
    CONNECT, SEND, RECEIVE, CLOSE = range(4)
    def __init__(self, type_, data=None):
        self.type_ = type_
        self.data = data

class ClientReply():
    ERROR, SUCCESS = range(2)
    def __init__(self, type_, data=None):
        self.type_ = type_
        self.data = data

class SocketClientThread(threading.Thread):
    def __init__(self, cmd_q=queue.Queue(), reply_q=queue.Queue()):
        super(SocketClientThread, self).__init__()
        self.cmd_q = cmd_q
        self.reply_q = reply_q
        self.alive = threading.Event()
        self.alive.set()
        self.socket = None

        self.handlers = {
            ClientCommand.CONNECT: self._handle_CONNECT,
            ClientCommand.CLOSE: self._handle_CLOSE,
            ClientCommand.SEND: self._handle_SEND,
            ClientCommand.RECEIVE: self._handle_RECEIVE,
        }

    def run(self):

        while self.alive.isSet():
            print("RUNNING")
            try:
                cmd = self.cmd_q.get(True, 0.1)
                self.handlers[cmd.type_](cmd)
            except queue.Empty as e:
                continue
            print(self.alive.isSet())

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)

    def _handle_CONNECT(self, cmd):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((cmd.data[0], cmd.data[1]))
            self.reply_q.put(self._success_reply())
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _handle_CLOSE(self, cmd):
        self.socket.close()
        reply = ClientReply(ClientReply.SUCCESS)
        self.reply_q.put(reply)

    def _handle_SEND(self, cmd):
        header = struct.pack('<L', len(cmd.data))
        try:
            print(f"[*] send data {header+cmd.data}")
            self.socket.sendall(header+cmd.data)
            self.reply_q.put(self._success_reply())
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _handle_RECEIVE(self, cmd):
        try:
            header_data = self._recv_n_bytes(4)
            if len(header_data) == 4:
                msg_len = struct.unpack('<L', header_data)[0]
                data = self._recv_n_bytes(msg_len)
                if len(data) == msg_len:
                    self.reply_q.put(self._success_reply(data))
                    return
            self.reply_q.put(self._error_reply('Socket closed prematurely'))
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _recv_n_bytes(self, n):
        data = b''
        while len(data) < n:
            chunk = self.socket.recv(n - len(data))
            if chunk == b'':
                break
            data += chunk
        return data

    def _error_reply(self, errstr):
        return ClientReply(ClientReply.ERROR, errstr)

    def _success_reply(self, data=None):
        return ClientReply(ClientReply.SUCCESS, data)

