import struct
import SocketServer
import json
import os
from base64 import b64encode
from hashlib import sha1
from mimetools import Message
from StringIO import StringIO
import thread
import base64
from visit import *
from GetJSON import *
import threading
import socket

import SocketServer

class TCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer): 
    allow_reuse_address = True

class WebSocketsHandler(SocketServer.StreamRequestHandler):
    magic = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        print "connection established", self.client_address
        self.handshake_done = False

    def handle(self):
        while True:
            if not self.handshake_done:
                self.handshake()
            else:
                self.read_next_message()

    def read_next_message(self):
        length = ord(self.rfile.read(2)[1]) & 127
        if length == 126:
            length = struct.unpack(">H", self.rfile.read(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self.rfile.read(8))[0]
        masks = [ord(byte) for byte in self.rfile.read(4)]
        decoded = ""
        for char in self.rfile.read(length):
            decoded += chr(ord(char) ^ masks[len(decoded) % 4])
        command = decoded
        res = json.loads(command)
        #exe python code
        if not os.path.isdir("_stuff"):
            os.mkdir("_stuff")
        try:
            exec(res["py"])
            using_sr = GetWindowInformation().usingScalableRendering == 1
            if using_sr:
                res["rtype"] = "image"
            if res["rtype"] == "image":
                swa = SaveWindowAttributes()
                swa.family = 0
                swa.format = swa.PNG
                swa.width  =  res["width"]
                swa.height =  res["height"]
                swa.fileName = "_stuff/vportal"
                SetSaveWindowAttributes(swa)
                r = SaveWindow()
                fimg = open(r,"rb")
                contents = fimg.read()
                encoded = "data:image/png;base64," + base64.b64encode(contents)
                if using_sr:
                    self.on_message("txt","here is your image result (perhaps forced by SR)")
                else:
                    self.on_message("txt","here is your image result")
                self.on_message("image",encoded)
            else:
                res = GetJSON()
                self.on_message("txt","here is your JSON result")
                self.on_message("json",res)
        except Exception as e:
            self.on_message("txt","<b><i>Python Exception: </i></b> " + str(e))

    def send_message(self, message):
        self.request.send(chr(129))
        length = len(message)
        if length <= 125:
            self.request.send(chr(length))
        elif length >= 126 and length <= 65535:
            self.request.send(chr(126))
            self.request.send(struct.pack(">H", length))
        else:
            self.request.send(chr(127))
            self.request.send(struct.pack(">Q", length))
        self.request.send(message)

    def handshake(self):
        data = self.request.recv(1024).strip()
        headers = Message(StringIO(data.split('\r\n', 1)[1]))
        if headers.get("Upgrade", None) != "websocket":
            return
        print 'Handshaking...'
        key = headers['Sec-WebSocket-Key']
        digest = b64encode(sha1(key + self.magic).hexdigest().decode('hex'))
        response = 'HTTP/1.1 101 Switching Protocols\r\n'
        response += 'Upgrade: websocket\r\n'
        response += 'Connection: Upgrade\r\n'
        response += 'Sec-WebSocket-Accept: %s\r\n\r\n' % digest
        self.handshake_done = self.request.send(response)
        print 'Handshake done.'

    def on_message(self, type, message):
        if message != "":
            res = { "rtype": type}
            if type == "txt":
                res["answer"] = message
            else:
                res["blob"] = message
            a = json.dumps(res)
            self.send_message(json.dumps(res))

if __name__ == "__main__":
    print socket.gethostname()
    server = TCPServer(
        ('', 9876), WebSocketsHandler)
    #    ("localhost", 8000), WebSocketsHandler)
    #    (socket.gethostname(), 9876), WebSocketsHandler)
    #server.serve_forever()
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
