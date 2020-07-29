import wifi
import audio
import system
import socket
import struct

# debug
import appconfig
import touchpads
import keypad
import display as dp

class _DisplayPackager:
    def __init__(self, tcp):
        self.tcp = tcp

    def flush(self, flags=None):
        desc = 'ii'
        p_data = struct.pack(desc, 0, flags)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def size(self):
        # TODO: server can not respond yet
        method = 1
        print("DISPKG: get size function not yet implemented")
        return

    def wsize(self, window):
        # TODO: server can not respond yet
        method = 2
        print("DISPKG: get wsize function not yet implemented")
        return

    def width(self):
        # TODO: server can not respond yet
        method = 3
        print("DISPKG: get width function not yet implemented")
        return

    def wwidth(self, window):
        # TODO: server can not respond yet
        method = 4
        print("DISPKG: get wwidth function not yet implemented")
        return

    def height(self):
        # TODO: server can not respond yet
        method = 5
        print("DISPKG: get height function not yet implemented")
        return

    def wheight(self, window):
        # TODO: server can not respond yet
        method = 6
        print("DISPKG: get wheight function not yet implemented")
        return

    def orientation(self, angle=None):
        if angle == None:
            # TODO: server can not respond yet
            method = 7
            print("DISPLG: get orientation function not yet implemented")
        else:
            desc = "ii"
            method = 8
            p_data = struct.pack(desc, method, angle)
            self.tcp.send_packaged_data(p_data, desc, packager=2)

    def worientation(self, window, angle=None):
        if angle == None:
            # TODO: server can not respond yet
            method = 9
            print("DISPLG: get worientation function not yet implemented")
        else:
            desc = "i" + str(len(window)) + "si"
            method = 10
            p_data = struct.pack(desc, method, window, angle)
            self.tcp.send_packaged_data(p_data, desc, packager=2)

    def getPixel(self, x, y):
        # TODO: server can not respond yet
        method = 11
        print("DISPKG: getPixel function not yet implemented")
        return

    def wgetPixel(self, window, x, y):
        # TODO: server can not respond yet
        method = 12
        print("DISPKG: wgetPixel function not yet implemented")
        return

    def drawRaw(self, x, y, width, height, data):
        desc = "iiiii" + str(len(data)) + "i"
        method = 13
        p_data = struct.pack("iiiii", method, x, y, width, height)
        for pixel in data:
            p_data.extend(struct.pack("i", pixel))
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def wdrawRaw(self, window, x, y, width, height, data):
        desc = "i" + str(len(window)) + "siiii" + str(len(data)) + "i"
        method = 14
        p_data = struct.pack("i" + str(len(window)) + "siiii", method, window, x, y, width, height)
        for pixel in data:
            p_data.extend(struct.pack("i", pixel))
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def drawPixel(self, x, y, color):
        desc = 'iiii'
        method = 15
        p_data = struct.pack(desc, method, x, y, color)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def wdrawPixel(self, window, x, y, color):
        desc = 'i' + str(len(window)) + 'siii'
        method = 16
        p_data = struct.pack(desc, method, window, x, y, color)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def drawFill(self, color):
        desc = 'ii'
        method = 17
        p_data = struct.pack(desc, method, color)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def wdrawFill(self, window, color):
        desc = 'i' + str(len(window)) + 'si'
        method = 18
        p_data = struct.pack(desc, method, window, color)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def drawLine(self, x0, y0, x1, y1, color):
        desc = 'iiiiii'
        method = 19
        p_data = struct.pack(desc, method, x0, y0, x1, y1, color)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def wdrawLine(self, window, x0, y0, x1, y1, color):
        desc = 'i' + str(len(window)) + 'siiiii'
        method = 20
        p_data = struct.pack(desc, method, window, x0, y0, x1, y1, color)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def drawRect(self, x, y, width, height, filled, color):
        desc = 'iiiii?i'
        method = 21
        p_data = struct.pack(desc, method, x, y, width, height, filled, color)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def wdrawRect(self, window, x, y, width, height, filled, color):
        desc = 'i' + str(len(window)) + 'siiii?i'
        method = 22
        p_data = struct.pack(desc, method, window, x, y, width, height, filled, color)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def drawCircle(self, x0, y0, radius, a0, a1, fill, color):
        desc = 'iiiiii?i'
        method = 23
        p_data = struct.pack(desc, method, x0, y0, radius, a0, a1, fill, color)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def wdrawCircle(self, window, x0, y0, radius, a0, a1, fill, color):
        desc = 'i' + str(len(window)) + 'siiiii?i'
        method = 24
        p_data = struct.pack(desc, method, window, x0, y0, radius, a0, a1, fill, color)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def drawText(self, x, y, text, color=None, font=None, x_scale=None, y_scale=None, window=None):
        _window_desc = str(len(window)) + "s" if not window == None else ""
        _desc = 'i' + _window_desc + 'ii' + str(len(text)) + 's'
        desc = _desc
        p_data = bytearray()
        method = 25
        if not color == None:
            desc += 'i'
            p_data.extend(struct.pack('i', color))
            method = 26
            if not font == None:
                size = str(len(font))
                desc += size + 's'
                p_data.extend(struct.pack(size + 's', font))
                method = 27
                if (not x_scale == None) and (not y_scale == None):
                    desc += 'ii'
                    p_data.extend(struct.pack('ii', x_scale, y_scale))
                    method = 28
        _p_data = bytearray()
        if window == None:
            _p_data = bytearray(struct.pack(_desc, method, x, y, text))
        else:
            method += 4
            _p_data = bytearray(struct.pack(_desc, method, window, x, y, text))
        _p_data.extend(p_data)
        self.tcp.send_packaged_data(_p_data, desc, packager=2)

    def wdrawText(self, window, x, y, text, color=None, font=None, x_scale=None, y_scale=None):
        self.drawText(x, y, text, color=color, font=font, x_scale=x_scale, y_scale=y_scale, window=window)

    def drawPng(self, x, y, png, window=None):
        # PNG can either be a string (filename) or data
        _window_desc = str(len(window)) + "s" if not window == None else ""
        desc = 'i' + _window_desc + 'ii' + str(len(png))
        p_data = bytearray()
        if isinstance(png, str):
            desc += 's'
            if window == None:
                p_data.extend(bytearray(struct.pack(desc, 33, x, y, png)))
            else:
                p_data.extend(bytearray(struct.pack(desc, 34, window, x, y, png)))
        else:
            if window == None:
                p_data.extend(bytearray(struct.pack('iii', 35, x, y)))
            else:
                p_data.extend(bytearray(struct.pack('i' + _window_desc + 'ii', 36, window, x, y)))
            desc += 'i'
            for pixel in data:
                p_data.extend(bytearray(struct.pack('i', pixel)))

        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def getTextWidth(self, text, font=None):
        # TODO: server can not respond yet
        method = 37
        print("DISPKG: getTextWidth funciton not yet implemented (maybe your device can do it by himself?)")
        return

    def getTextHeight(self, text, font=None):
        # TODO: server can not respond yet
        method = 38
        print("DISPKG: getTextHeight funciton not yet implemented (maybe your device can do it by himself?)")
        return

    def pngInfo(self, png):
        # TODO: server can not respond yet
        method = 39
        print("DISPKG: pngInfo funciton not yet implemented (maybe your device can do it by himself?)")
        return

    def windowCreate(self, name, width, height):
        desc = 'i' + str(len(name)) + 'sii'
        method = 40
        p_data = struct.pack(desc, method, name, width, height)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def windowRemove(self, name):
        desc = 'i' + str(len(name)) + 's'
        method = 41
        p_data = struct.pack(desc, method, name)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def windowMove(self, name, width, height):
        desc = 'i' + str(len(name)) + 'sii'
        method = 42
        p_data = struct.pack(desc, method, name, width, height)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def windowResize(self, name, width, height):
        desc = 'i' + str(len(name)) + 'sii'
        method = 43
        p_data = struct.pack(desc, method, name, width, height)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def windowVisibility(self, name, visible=False):
        if visible:
            desc = 'i' + str(len(name)) + 's?'
            method = 44
            p_data = struct.pack(desc, method, name, visible)
            self.tcp.send_packaged_data(p_data, desc, packager=2)
        else:
            desc = 'i' + str(len(name)) + 's'
            method = 45
            p_data = struct.pack(desc, method, name)
            self.tcp.send_packaged_data(p_data, desc, packager=2)

    def windowShow(self, name):
        desc = 'i' + str(len(name)) + 's'
        method = 46
        p_data = struct.pack(desc, method, name)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def windowHide(self, name):
        desc = 'i' + str(len(name)) + 's'
        method = 47
        p_data = struct.pack(desc, method, name)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def windowFocus(self, name):
        desc = 'i' + str(len(name)) + 's'
        method = 48
        p_data = struct.pack(desc, method, name)
        self.tcp.send_packaged_data(p_data, desc, packager=2)

    def windowList(self):
        # TODO: server can not respond yet
        print("DISPKG: windowList funciton not yet implemented")
        return
        desc = 'i'
        method = 49
        p_data = struct.pack(desc, method)
        #self.tcp.send_packaged_data(p_data, desc, packager=2)

class _RGBPackager:
    def __init__(self, tcp):
        self.tcp = tcp
        self.FONT_7x5 = 0
        self.FONT_6x3 = 1

    def clear(self):
        self.tcp.send_data(0, 'i', packager=3)

    def background(self, rgbt):
        p_data = struct.pack('iiii', 1, rgbt[0], rgbt[1], rgbt[2])
        self.tcp.send_packaged_data(p_data, 'iiii', packager=3)

    def getbrightness(self):
        # TODO: server can not respond yet
        # self.tcp.send_data(2, 'i', packager=3)
        # receive data
        print("RGBPKG: getbrightness function not yet implemented")
        return

    def setbrightness(self, brightness):
        p_data = struct.pack('ii', 3, brightness)
        self.tcp.send_packaged_data(p_data, 'ii', packager=3)

    def framerate(self, framerate):
        p_data = struct.pack('ii', 4, framerate)
        self.tcp.send_packaged_data(p_data, 'ii', packager=3)

    def pixel(self, rgbt, xyt):
        desc = 'iiiiii'
        p_data = struct.pack(desc, 5, rgbt[0], rgbt[1], rgbt[2], xyt[0], xyt[1])
        self.tcp.send_packaged_data(p_data, desc, packager=3)

    def text(self, string, rgbt, xyt = (0, 0)):
        desc = "i" + str(len(string)) + "siiiii"
        p_data = struct.pack(desc, 6, string, rgbt[0], rgbt[1], rgbt[2], xyt[0], xyt[1])
        self.tcp.send_packaged_data(p_data, desc, packager=3)

    def scrolltext(self, string, rgbt, xyt = (0, 0), width = 32):
        desc = "i" + str(len(string)) + "siiiiii"
        p_data = struct.pack(desc, 7, string, rgbt[0], rgbt[1], rgbt[2], xyt[0], xyt[1], width)
        self.tcp.send_packaged_data(p_data, desc, packager=3)

    def image(self, data, xyt, wht):
        desc = "iiiii" + str(len(data)) + "i"
        p_data = bytearray(struct.pack("iiiii", 8, xyt[0], xyt[1], wht[0], wht[1]))
        for pixel in data:
            p_data.extend(bytearray(struct.pack('i', pixel)))
        self.tcp.send_packaged_data(p_data, desc, packager=3)

    def gif(self, data, xyt, wht, frames):
        desc = "iiiiii" + str(len(data)) + "i"
        p_data = bytearray(struct.pack("iiiiii", 9, xyt[0], xyt[1], wht[0], wht[1], frames))
        for pixel in data:
            p_data.extend(bytearray(struct.pack('i', pixel)))
        self.tcp.send_packaged_data(p_data, desc, packager=3)

    def setfont(self, font):
        desc = "ii"
        p_data = struct.pack(desc, 10, font)
        self.tcp.send_packaged_data(p_data, desc, packager=3)

    def textwidth(self, text):
        # TODO: server can not respond yet
        # desc = "i" + str(len(text))
        # p_data = struct.pack(desc, 11, text)
        # self.tcp.send_packaged_data(p_data, desc, packager=3)
        # receive data
        print("RGBPKG: textwidth function not yet implemented")
        return

    def disablecomp(self):
        self.tcp.send_data(12, 'i', packager=3)

    def enablecomp(self):
        self.tcp.send_data(13, 'i', packager=3)

    def frame(self, data):
        desc = "i" + str(len(data)) + "i"
        p_data = bytearray(struct.pack('i', 14))
        for pixel in data:
            p_data.extend(bytearray(struct.pack('i', pixel)))
        self.tcp.send_packaged_data(p_data, desc, packager=3)

class CZ20_TCP_Client:
    def __init__(self):
        self._connect_wifi()
        self.rgb = _RGBPackager(self)
        self.display = _DisplayPackager(self)

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

    def reconnect(self, host=None, port=None):
        self._announce("TCP: Reconnecting")
        self.stop()
        self.connect(host=host, port=port)

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
page = 0

if __name__ == "tcp_client":
    def load_settings():
        global settings
        settings = appconfig.get("tcp_client", {"server_ip": "192.168.1.4", "server_port": 1234})
        print("Server IP: " + settings["server_ip"] + " port: " + str(settings["server_port"]))

    def on_key(k, p):
        global tcp
        global page
        if p:
            if page == 0:
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
            elif page == 1:
                x,y = k % 4, int(k / 4)
                if k == 0:
                    tcp.rgb.clear()
                if k == 1:
                    tcp.rgb.disablecomp()
                if k == 2:
                    tcp.rgb.enablecomp()
                if k == 3:
                    tcp.rgb.frame([4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 255, 255, 255, 255, 255, 255, 255, 255, 4227327, 4227327, 4227327, 255, 255, 4227327, 4227327, 4227327, 4278190335, 4227327, 4227327, 4227327, 4227327, 4278190335, 4278190335, 4278190335, 4278190335, 4227327, 4227327, 4227327, 4227327, 4278190335, 4278190335, 255, 4286644223, 4286644223, 4286644223, 4286644223, 4278223103, 4286644223, 255, 2155905279, 255, 255, 255, 2155905279, 255, 4227327, 4227327, 4227327, 4286578943, 4278190335, 4278190335, 4278190335, 4278190335, 4286578943, 4286578943, 4286578943, 4286578943, 4278190335, 4278190335, 4278190335, 4278190335, 4286578943, 4286578943, 255, 4286644223, 4278223103, 4286644223, 4286644223, 4286644223, 255, 2155905279, 4294967295, 255, 2155905279, 4294967295, 255, 2155905279, 255, 4227327, 4227327, 4294902015, 4286578943, 4286578943, 4286578943, 4286578943, 4294902015, 4294902015, 4294902015, 4294902015, 4286578943, 4286578943, 4286578943, 4286578943, 4294902015, 4294902015, 255, 4286644223, 4286644223, 4286644223, 4278223103, 4286644223, 255, 2155905279, 255, 255, 2155905279, 255, 255, 2155905279, 255, 4227327, 4227327, 16711935, 4294902015, 4294902015, 4294902015, 4294902015, 16711935, 16711935, 16711935, 16711935, 4294902015, 4294902015, 4294902015, 4294902015, 16711935, 16711935, 255, 4286644223, 4286644223, 4286644223, 4286644223, 4286644223, 255, 4286611711, 2155905279, 2155905279, 2155905279, 2155905279, 2155905279, 4286611711, 255, 4227327, 4227327, 8454143, 16711935, 16711935, 16711935, 16711935, 8454143, 8454143, 8454143, 8454143, 16711935, 16711935, 16711935, 16711935, 8454143, 8454143, 255, 4286644223, 4278223103, 4286644223, 4286644223, 4278223103, 4286644223, 255, 2155905279, 2155905279, 2155905279, 2155905279, 2155905279, 255, 4227327, 4227327, 4227327, 2147549183, 8454143, 8454143, 8454143, 8454143, 2147549183, 2147549183, 2147549183, 2147549183, 8454143, 8454143, 8454143, 8454143, 2147549183, 2147549183, 2147549183, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 4227327, 4227327, 4227327, 4227327, 4227327, 2147549183, 2147549183, 2147549183, 2147549183, 4227327, 4227327, 4227327, 4227327, 2147549183, 2147549183, 2147549183, 2147549183, 4227327, 4227327, 4227327, 4227327, 2147549183, 2147549183, 2147549183, 2147549183, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327, 4227327])
                if k == 4:
                    tcp.rgb.pixel((40,40,255), (3, 3))
                if k == 5:
                    tcp.rgb.text("Hello World", (150, 0, 0))
                if k == 6:
                    tcp.rgb.scrolltext("Hello World", (0, 150, 0))
                if k == 7:
                    tcp.rgb.image([0x00FF00FF,0x00FF00FF,0x00FF00FF, 0xFF0000FF, 0xFF0000FF, 0xFF0000FF],
                                  (0,0), (3,2))
                if k == 8:
                    tcp.rgb.gif([0x00FF00FF,0x00FF00FF,0x00FF00FF, 0xFF0000FF, 0xFF0000FF, 0xFF0000FF],
                                (10, 1), (3,1), 2)
                if k == 9:
                    tcp.rgb.setfont(tcp.rgb.FONT_6x3)
                if k == 10:
                    tcp.rgb.setfont(tcp.rgb.FONT_7x5)

                if x == 0 and y == 3:
                    print("restarting")
                    dp.drawFill(0xa15b00)
                    system.start(system.currentApp())
                if x == 3 and y == 3:
                    print("reconnecting")
                    tcp.reconnect()


    def clear():
        for i in range(5):
            print("")

    def on_left(p):
        global page
        page = 0

    def on_right(p):
        global page
        page = 1

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

    touchpads.on(touchpads.LEFT, on_left)
    touchpads.on(touchpads.RIGHT, on_right)

