import rgb
import socket
import struct
import wifi
import network
import time

DEBUG = False
IP_WAIT_DELAY_BETWEEN_TRIES_MS =  500
MAX_IP_SECONDS_WAIT = 50

class _RGBUnpackager:
    def unpack(self, _p_data, _desc):
        ba = bytearray(_p_data)
        method = struct.unpack('i', ba[:4])[0]
        p_data = ba[4:]
        print("PKGRGB: method: " + str(method))

        desc = _desc[1:]
        print("PKGRGB: desc: " + desc)

        if method == 0:
            rgb.clear()

        elif method == 1:
            (r, g, b) = struct.unpack('iii', p_data)
            rgb.background((100,100,100))

        elif method == 2:
            # TODO: can not respond yet
            # rgb.getbrightness()
            pass

        elif method == 3:
            brightness = struct.unpack('i', p_data)[0]
            rgb.setbrightness(brightness)

        elif method == 4:
            framerate = struct.unpack('i', p_data)[0]
            rgb.framerate(framerate)

        elif method == 5:
            (r,g,b,x,y) = struct.unpack('iiiii', p_data)
            rgb.pixel((r,g,b),(x,y))

        elif method == 6:
            (string, r, g, b, x, y) = struct.unpack(desc, p_data)
            # default (x,y) = (0,0)
            rgb.text(string, (r,g,b), (x,y))

        elif method == 7:
            (string, r, g, b, x, y, width) = struct.unpack(desc, p_data)
            # default (x,y) = (0,0)
            # default width = whole screen == 32
            rgb.scrolltext(string, (r,g,b), (x,y), width)

        elif method == 8:
            size = struct.calcsize('iiii')
            (x,y,w,h) = struct.unpack('iiii', p_data[0:size])
            data = list(struct.unpack(desc[4:], p_data[size:]))
            rgb.image(data, (x,y), (w,h))

        elif method == 9:
            size = struct.calcsize('iiiii')
            (x,y,w,h, frames) = struct.unpack('iiiii', p_data[0:size])
            data = list(struct.unpack(desc[5:], p_data[size:]))
            rgb.gif(data, (x,y), (w,h), frames)

        elif method == 10:
            font = struct.unpack(desc, p_data)[0]
            rgb.setfont(font)

        elif method == 11:
            # TODO: can not respond yet
            # rgb.textwidht(text)
            pass

        elif method == 12:
            rgb.disablecomp()

        elif method == 13:
            rgb.enablecomp()

        elif method == 14:
            data = list(struct.unpack(desc, p_data))
            rgb.frame(data)

class _RawUnpackager:
    def __init__(self, int32Handler=None, floatHandler=None, doubleHandler=None, stringHandler=None):
        self.int32Handler  = int32Handler  if not int32Handler  == None else self.rawRGB
        self.floatHandler  = floatHandler  if not floatHandler  == None else self.rawRGB
        self.doubleHandler = doubleHandler if not doubleHandler == None else self.rawRGB
        self.stringHandler = stringHandler if not stringHandler == None else self.rawRGB

    def unpack(self, p_data, descriptor):
        data = list(struct.unpack(descriptor, p_data))[0]

        if descriptor == 'i':
            self.int32Handler(data)
        elif descriptor == 'f':
            self.floatHandler(data)
        elif descriptor == 'd':
            self.doubleHandler(data)
        else:
            self.stringHandler(data.decode('utf-8'))

    def rawRGB(self, data):
        rgb.clear()
        rgb.scrolltext(str(data), (0, 71, 150)) # I like oceanblue

class CZ19_TCP_Server:
    def __init__(self, rawUnpackager=None):
        rgb.setfont(rgb.FONT_6x3)
        self.raw = rawUnpackager if not rawUnpackager == None else _RawUnpackager()
        self.rgb_unpack = _RGBUnpackager()

        self.open = False
        status_rgb = (81, 147, 252)

        rgb.clear()
        rgb.scrolltext("Starting TCP Server", status_rgb)
        self._announce("Starting TCP Server")

        rgb.clear()
        rgb.scrolltext("Connecting WiFi", status_rgb)
        print("Connecting WiFi")
        if not wifi.status():
            wifi.connect()

        rgb.clear()
        rgb.text("Get IP " + str(MAX_IP_SECONDS_WAIT))
        s = network.WLAN(network.STA_IF)
        self.ip = list(s.ifconfig())[0]

        tries = 0
        max_tries = MAX_IP_SECONDS_WAIT * 1000 / IP_WAIT_DELAY_BETWEEN_TRIES_MS
        while self.ip == "0.0.0.0" and tries < max_tries:
            print("Wrong ip: " + self.ip + " try: " + str(tries))
            time.sleep_ms(IP_WAIT_DELAY_BETWEEN_TRIES_MS)
            rgb.text("Get IP " + str(MAX_IP_SECONDS_WAIT - int(1000 / IP_WAIT_DELAY_BETWEEN_TRIES_MS * tries)))
            self.ip = list(s.ifconfig())[0]
            tries = tries + 1

        rgb.clear()
        text = "IP: " + str(self.ip)
        print("IP: " + str(self.ip))
        rgb.scrolltext(text, status_rgb)

        rgb.setfont(rgb.FONT_7x5)
        print("Startup finished")

    def _announce(self, string):
        print()
        print("================")
        print(string)

    def start(self, callback=None, port=1234):
        print("Opening socket")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, port))
        self.sock.listen(1)
        self.open = True
        self.callback = callback

        while self.open:
            self._announce("TCP: Waiting for new connection")

            conn, client = self.sock.accept()

            print("TCP: Connection found!")

            try:
                while self.open:
                    self._announce("TCP: Waiting for package")

                    p_meta = conn.recv(struct.calcsize('ii'))
                    if not p_meta:
                        print("TCP: Failed meta response")
                        break

                    desc_size, packager = struct.unpack('ii', p_meta)
                    print("TCP: Desc size: " + str(desc_size))

                    p_desc = conn.recv(desc_size)
                    if not p_desc:
                        print("TCP: Failed descriptor size")
                        break
                    encoded_desc = struct.unpack(str(desc_size) + 's', p_desc)
                    desc = list(encoded_desc)[0].decode('utf-8')
                    print("TCP: Desc: " + str(desc))

                    p_data = conn.recv(struct.calcsize(desc))
                    if not p_data:
                        print("TCP: Failed data")
                        break

                    self.package_handler(p_data, desc, packager)

            finally:
                conn.close()

    def close(self):
        self.open = False
        self.sock.close()

    def package_handler(self, p_data, descriptor, packager):
        print("PKG: descriptor: " + descriptor + "'")
        #print("PKG: data: '" + str(p_data) + "'")

        if packager == 0:
            if self.callback == None:
                print("PKGERROR: no callback given whilst requested to unpackage with callback")
                return

            self.callback(p_data, descriptor)
        elif packager == 1: # Raw data (strings, integers, floats, doubles)
            self.raw.unpack(p_data, descriptor)

        #elif packager == 2: # display library

        elif packager == 3: # RGB library
            self.rgb_unpack.unpack(p_data, descriptor)

if __name__ == "tcp_lib":
    if not DEBUG:
        try:
            tcpServer = CZ19_TCP_Server()
            tcpServer.start()
        except Exception as e:
            import system, sys
            sys.print_exception(e)
            system.crashedWarning()
            #system.sleep()
        finally:
            tcpServer.close()

    else:
        print("debug is online, waiting for server to be started")
