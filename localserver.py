#!/usr/bin/env python3
import socket
import struct
import signal
import sys
import re

def announce(string):
    print()
    print("================")
    print(string)

class TCPServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.open = False

        self.struct_desc_size = struct.Struct('i')

    def start(self, callback, port=1234):
        self.sock.bind(("192.168.1.4", port))
        self.sock.listen(1)
        self.open = True

        while self.open:
            announce("TCP: Waiting for new connection")

            conn, client = self.sock.accept()

            print("TCP: Connection found!")

            try:
                while self.open:
                    announce("TCP: Waiting for package")

                    p_desc_size = conn.recv(self.struct_desc_size.size)
                    if not p_desc_size:
                        print("TCP: Failed descriptor size response")
                        break
                    desc_size = list(self.struct_desc_size.unpack(p_desc_size))[0]
                    print("TCP: Desc size: " + str(desc_size))

                    p_desc = conn.recv(desc_size)
                    if not p_desc:
                        print("TCP: Failed descriptor size")
                        break
                    desc = list(struct.unpack(str(desc_size) + 's', p_desc))[0].decode('utf-8')
                    print("TCP: Desc: " + str(desc))

                    p_data = conn.recv(struct.calcsize(desc))
                    if not p_data:
                        print("TCP: Failed data")
                        break

                    (response) = struct.unpack(desc, p_data)

                    print("Type: " + str(type(response)))

                    callback(response, desc)

                    #self.recv_pkg(connection)
            finally:
                conn.close()

    def stop(self):
        self.open = False
        self.sock.close()


def signal_handler(sig, frame):
    print("Closing socket")
    global tcpserver
    tcpserver.stop()
    print("Closed socket")
    sys.exit(0)

def package_handler(data, descriptor):
    p = re.compile('[0-9]+s')
    match = p.match(descriptor)

    if match:
        if match.start() == 0 and match.end() == len(descriptor):
            print("PKG: Received string!")


signal.signal(signal.SIGINT, signal_handler)

tcpserver = TCPServer()
tcpserver.start(package_handler)
