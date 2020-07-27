import wifi
import audio
import system
import display as dp
import keypad
import socket
import struct

# debug
import appconfig

class CZ20_TCP_Client:
    def __init__(self):
        self._connect_wifi()

    def _announce(self, string):
        print()
        print("================")
        print(string)

    def _connect_wifi(self):
        dp.drawPixel(0,0, 0x0044BB)
        dp.flush()
        if not wifi.status():
            audio.play('/cache/system/wifi_connecting.mp3')
            wifi.connect()

            dp.drawPixel(1,0, 0x0044BB)
            dp.flush()

            wifi.wait()
            if not wifi.status():
                dp.drawLine(0,0, 1,0, 0xFF0000)
                dp.flush()
                audio.play('/cache/system/wifi_failed.mp3', on_finished=system.launcher)

    def connect(self, host=None, port=None):
        if host != None:
            self.host = host

        if port != None:
            self.port = port

        self._announce("TCP: Connecting to " + str(self.host) + ":" + str(self.port))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def stop(self):
        self._announce("TCP: Stopping")
        self.sock.close()

    def reconnect(self):
        self._announce("TCP: Reconnecting")
        self.stop()
        self.connect()

    def send_packaged_data(self, p_data, data_descriptor, packager=0):
        ## TODO: compact this to one single "package"
        print("TCP: Sending package: " + data_descriptor)

        # first 2 bites: size of data descriptor, packaging type function
        desc_size = struct.pack('ii', len(data_descriptor), packager)
        self.sock.sendall(desc_size)

        # second block: data descriptor
        desc = struct.pack(str(len(data_descriptor)) + 's', data_descriptor)
        self.sock.sendall(desc)

        # third block: data
        self.sock.sendall(p_data)

    def send_data(self, data, data_descriptor, packager=0):
        packed_data = struct.pack(data_descriptor, data)
        self.send_packaged_data(packed_data, data_descriptor, packager)

    def send_text(self, string):
        self.send_data(string, str(len(string)) + 's', 1)

    def send_int32(self, i):
        self.send_data(i, 'i', 1)

    def send_float(self, f):
        self.send_data(f, 'f', 1)

    def send_double(self, d):
        self.send_data(d, 'd', 1)

settings = None
tcp = None

def load_settings():
    global settings
    settings = appconfig.get("tcp_client", {"server_ip": "192.168.1.4", "server_port": 1234})
    print("Server IP: " + settings["server_ip"] + " port: " + str(settings["server_port"]))

def on_key(k, p):
    global tcp
    if p:
        x,y = k % 4, int(k / 4)
        if (x == 0 and y == 0):
            tcp.send_text("red")
        if (x == 1 and y == 0):
            tcp.send_text("green")
        if (x == 2 and y == 0):
            tcp.send_text("blue")

        if (x == 0 and y == 1):
            tcp.send_int32(42)
        if (x == 1 and y == 1):
            tcp.send_int32(-10)
        if (x == 2 and y == 1):
            tcp.send_int32(2147483647)

        if (x == 0 and y == 2):
            tcp.send_float(0)
        if (x == 1 and y == 2):
            tcp.send_double(0)
        if (x == 2 and y == 2):
            print("noh")

        if x == 0 and y == 3:
            print("restarting")
            dp.drawFill(0xa15b00)
            system.start(system.currentApp())
        if x == 3 and y == 3:
            print("reconnecting")
            tcp.reconnect()
        #print("key:" + str(k) + " coords x:" + str(x) + " y:" + str(y))

def clear():
    for i in range(5):
        print("")

if __name__ == "tcp_client":
    r=0xa10000
    g=0x23a100
    b=0x0010a1

    clear()
    load_settings()

    tcp = CZ20_TCP_Client()
    tcp.connect(settings["server_ip"], settings["server_port"])

    dp.drawPixel(0,0, r)
    dp.drawPixel(1,0, r)
    dp.drawPixel(2,0, r)
    dp.drawPixel(0,1, g)
    dp.drawPixel(1,1, g)
    dp.drawPixel(2,1, g)
    dp.drawPixel(0,2, b)
    dp.drawPixel(1,2, b)
    dp.drawPixel(2,2, b)
    dp.drawPixel(3,3, 0xBB004B)
    dp.drawPixel(0,3, 0xE3A300)
    dp.flush()

    keypad.add_handler(on_key)
