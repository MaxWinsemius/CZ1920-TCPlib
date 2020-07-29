import socket
import struct
import wifi
import network
import time
import rgb
import display

DEBUG = False
IP_WAIT_DELAY_BETWEEN_TRIES_MS =  500
MAX_IP_SECONDS_WAIT = 50

class _DisplayUnpackager:
    def unpack(self, _p_data, _desc):
        ba = bytearray(_p_data)
        method = struct.unpack('i', ba[:4])[0]
        desc = _desc[1:]
        p_data = ba[4:]
        print("PKGDIS: method: " + str(method))
        print("PKGDIS: desc: " + desc)

        if method == 0:
            flags = struct.unpack('i', p_data)
            display.flush(flags)

        elif method == 8:
            angle = struct.unpack(desc, p_data)[0]
            display.orientation(angle)

        elif method == 10:
            window, angle = struct.unpack(desc, p_data)
            window = window.decode()
            display.orientation(window.decode(), angle)

        elif method == 13:
            size = struct.calcsize('iiii')
            x, y, widh, height = struct.unpack('iiii', p_data[:size])
            data = list(struct.unpack(desc[4:], p_data[size:]))
            display.drawRaw(x, y, width, height, data)

        elif method == 14:
            loc = desc.find('s')
            window, x, y, width, height = struct.unpack(desc[:loc+5], p_data[:struct.calcsize(desc[:loc+5])])
            window = window.decode()
            data = list(struct.unpack(desc[loc+5:], p_data[:struct.calcsize(desc[:loc+5])]))
            display.drawRaw(window, x, y, width, height, data)

        elif method == 15:
            x, y, color = struct.unpack(desc, p_data)
            display.drawPixe(x, y, color)

        elif method == 16:
            window, x, y, color = struct.unpack(desc, p_data)
            window = window.decode()
            display.drawPixel(window, x, y, color)

        elif method == 17:
            color = struct.unpack(desc, p_data)[0]
            display.drawFill(color)

        elif method == 18:
            window, color = struct.unpack(desc, p_data)[0]
            window = window.decode()
            display.drawFill(window, color)

        elif method == 19:
            x0, y0, x1, y1, color = struct.unpack(desc, p_data)
            display.drawLine(x0, y0, x1, y1, color)

        elif method == 20:
            window, x0, y0, x1, y1, color = struct.unpack(desc, p_data)
            window = window.decode()
            display.drawLine(window, x0, y0, x1, y1, color)

        elif method == 21:
            x, y, width, height, filled, color = struct.unpack(desc, p_data)
            display.drawRect(x, y, width, height, filled, color)

        elif method == 22:
            window, x, y, width, heght, filled, color = struct.unpack(desc, p_data)
            window = window.decode()
            display.drawRect(window, x, y, width, height, filled, color)

        elif method == 23:
            x0, y0, radius, a0, a1, fill, color = struct.unpack(desc, p_data)
            display.drawCircle(x0, y0, radius, a0, a1, fill, color)

        elif method == 24:
            window, x0, y0, radius, a0, a1, fill, color = struct.unpack(desc, p_data)
            window = window.decode()
            display.drawCircle(window, x0, y0, radius, a0, a1, fill, color)

        elif method > 24 and method < 33:
            # what a lovely abomanation of code has this become
            window = None
            if method > 28:
                method -= 4
                loc = desc.find('s') + 1
                window = struct.unpack(desc[:loc], p_data[:struct.calcsize(desc[:loc])])[0]
                window = window.decode()
                p_data = p_data[struct.calcsize(desc[:loc]):]
                desc = desc[loc:]

            loc = desc.find('s') + 1
            x, y, text = struct.unpack(desc[:loc], p_data[:struct.calcsize(desc[:loc])])
            text = text.decode()
            p_data = p_data[struct.calcsize(desc[:loc]):]
            desc = desc[loc:]

            if method > 25:
                color = struct.unpack('i', p_data[:struct.calcsize('i')])
                p_data = p_data[struct.calcsize('i'):]
                desc = desc[1:]

                if method > 26:
                    loc = desc.find('s') + 1
                    font = struct.unpack(desc[:loc], p_data[:struct.calcsize(desc[:loc])])[0]
                    font = font.decode()
                    p_data = p_data[struct.calcsize(desc[:loc]):]
                    desc = desc[loc:]

                    if method > 27:
                        x_scale, y_scale = struct.unpack(desc, p_data)
                        if window == None:
                            display.drawText(x, y, text, color, font, x_scale, y_scale)
                        else:
                            display.drawText(window, x, y, text, color, font, x_scale, y_scale)
                    else:
                        if window == None:
                            display.drawText(x, y, text, color, font)
                        else:
                            display.drawText(window, x, y, text, color, font)
                else:
                    if window == None:
                        display.drawText(x, y, text, color)
                    else:
                        display.drawText(window, x, y, text, color)
            else:
                if window == None:
                    display.drawText(x, y, text)
                else:
                    display.drawText(window, x, y, text)

        elif method == 33:
            x, y, png = struct.unpack(desc, p_data)
            png = png.decode()
            display.drawPng(x, y, png)

        elif method == 34:
            window, y, png = struct.unpack(desc, p_data)
            window = window.decode()
            png = png.decode()
            display.drawPng(window, x, y, png)

        elif method == 35:
            x, y = struct.unpack('ii', p_data[:struct.calcsize('ii')])
            png = list(struct.unpack(desc[2:], p_data[struct.calcsize('ii'):]))
            display.drawPng(x, y, png)

        elif method == 36:
            window, x, y = struct.unpack('ii', p_data[:struct.calcsize('ii')])
            window = window.decode()
            png = list(struct.unpack(desc[2:], p_data[struct.calcsize('ii'):]))
            display.drawPng(window, x, y, png)

        elif method == 40:
            name, width, height = struct.unpack(desc, p_data)
            name = name.decode()
            display.windowCreate(name, width, height)

        elif method == 41:
            name = struct.unpack(desc, p_data)[0]
            name = name.decode()
            display.windowRemove(name)

        elif method == 42:
            name, width, height = struct.unpack(desc, p_data)
            name = name.decode()
            display.windowMove(name, width, height)

        elif method == 43:
            name, width, height = struct.unpack(desc, p_data)
            name = name.decode()
            display.windowResize(name, width, height)

        elif method == 44:
            name, visible = struct.unpack(desc, p_data)
            name = name.decode()
            display.windowVisibility(name, visible)

        elif method == 45:
            name = struct.unpack(desc, p_data)
            name = name.decode()
            display.windowVisibility(name)

        elif method == 46:
            name = struct.unpack(desc, p_data)
            name = name.decode()
            display.windowShow(name)

        elif method == 47:
            name = struct.unpack(desc, p_data)
            name = name.decode()
            display.windowHide(name)

        elif method == 48:
            name = struct.unpack(desc, p_data)
            name = name.decode()
            display.windowFocus(name)

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
