import rgb
import socket
import struct
import re
import wifi
import network

def announce(string):
    print()
    print("================")
    print(string)

class CZ19_TCP_Server:
    def __init__(self):
        self.open = False
        status_rgb = (81, 147, 252)

        rgb.clear()
        rgb.scrolltext("Starting TCP Server", status_rgb)
        announce("Starting TCP Server")

        rgb.clear()
        rgb.scrolltext("Connecting WiFi", status_rgb)
        print("Connecting WiFi")
        if not wifi.status():
            wifi.connect()

        rgb.clear()
        s = network.WLAN(network.STA_IF)
        self.ip, sub, gateway, dns = s.ifconfig()
        text = "IP: " + str(self.ip)
        print("IP: " + str(self.ip))
        rgb.scrolltext(text, status_rgb)

        print("Startup finished")


    def start(self, callback, port=1234):
        print("Opening socket")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, port))
        self.sock.listen(1)
        self.open = True

        while self.open:
            announce("TCP: Waiting for new connection")

            conn, client = self.sock.accept()

            print("TCP: Connection found!")

            try:
                while self.open:
                    announce("TCP: Waiting for package")

                    p_desc_size = conn.recv(struct.calcsize('i'))
                    if not p_desc_size:
                        print("TCP: Failed descriptor size response")
                        break
                    desc_size = list(struct.unpack('i', p_desc_size))[0]
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

                    print("Type: " + str(type(p_data)))

                    callback(p_data, desc)

            finally:
                conn.close()

    def close(self):
        self.open = False
        self.sock.close()

def package_handler(p_data, descriptor):
    print("PKG: descriptor: '" + descriptor + "'")
    print("PKG: data: '" + str(p_data) + "'")

    # check if string
    p = re.compile('^[0-9]+s$')
    match = p.match(descriptor)
    if match:
        print("PKG: Received string!")
        string = list(struct.unpack(descriptor, p_data))[0].decode('utf-8')
        print("PKG: stringdata: " + string)
        rgb.clear()
        rgb.scrolltext(string, (187, 0, 75))


#try:
#    tcpServer = CZ19_TCP_Server()
#    tcpServer.start(package_handler)
#except Exception as e:
#    import system, sys
#    sys.print_exception(e)
#    system.crashedWarning()
#    system.sleep()
#finally:
#    tcpServer.close()
