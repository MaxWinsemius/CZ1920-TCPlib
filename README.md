# CZ1920 TCPlib

A library to share data between the Campzone 2019 HackerZones and Campzone 2020 Hackerzone badges. 

## Usage
### Installation
- Install https://badge.team/projects/cz1920_tcplib on your CZ20 badge.
- Install https://badge.team/projects/cz1920_tcplib_cz19_version/ on your CZ19 badge.

#### IP Address
If you're modifying the source of the CZ20 code you can change the ip address simply the following way: get the ip-address from your CZ19 badge and set this ip address to the `server_ip` in your CZ20 badge at [the webusb settings page](webusb.hackz.one/settings).

Otherwise change the host when starting the `CZ20_TCP_Client`.

### Server startup
- Start the server (CZ19 badge).
- Start the client (CZ20 badge).
- Press the top row of buttons and see changes!

### Using the library
#### importing the library
```
import apps.cz1920_tcplib as tcpclient              # On the CZ20 badge library
import apps.cz1920_tcplib_cz19_version as tcpserver # On the CZ19 badge library
```
#### CZ20 badge
##### Starting the client / setting up a different host
```
tcp_client = tcpclient.CZ20_TCP_Client()
tcp_client.connect(host=<ip of your CZ19 badge>, port=None)
```

By giving any values to any of these parameters you will overwrite the previously set ones and the tcp server will connect to the new address.

(Note: if there is no server running on this connection, the client will crash trying to get a tcp connection up).

##### Stopping the client
```
tcp_client.stop()
```

##### Reconnecting the client
```
tcp_client.reconnect()
```

Todo: allow for new host and port settings

##### Prebuild data handling
```
tcp_client.send_text(string)
tcp_client.send_int32(i)
tcp_client.send_float(f)
tcp_client.send_double(d)
```

##### The Display library
> This library has not been fully tested. If you encounter bugs, please report with an issue or ping me at discord (Hernivo)

> The display library can be over-drawn by the RGB library. Run `tcp_client.rgb.disablecomp()` beforehand if you want to use it.

```
tcp_client.display.flush() # draws buffer to the screen, such as you would do on the CZ19 badge with display.clear()
```

Most other [methods](https://docs.badge.team/esp32-app-development/api-reference/display/) work the same way. If you want to write to a window, use the normal funcion name but with a `w` in front of it:
```
display.drawPixel("myWindow", 0, 0, 0xBB004B) becomes tcp_client.display.wdrawPixel("myWindow", 0, 0, 0xBB004B)
```

Supported functions:
- `tcp_client.display.flush([flags])`
- `tcp_client.display.orientation(angle)` (note that it can not request an angle, but only write)
- `tcp_client.display.getPixel(x, y)`
- `tcp_client.display.drawRaw(x, y, width, height, data)`
- `tcp_client.display.drawPixel(x, y, color)`
- `tcp_client.display.drawFill(color)`
- `tcp_client.display.drawLine(x0, x1, y0, y1, color)`
- `tcp_client.display.drawRect(x, y, width, height, filled, color)`
- `tcp_client.display.drawCircle(x0, y0, radius, a0, a1, fill, color)`
- `tcp_client.display.drawText(x, y, text, [color], [font], [x_scale], [y_scale])` (I think this method took about 30% of the time of writing this display library)
- `tcp_client.display.drawPng(x, y, [data or filename])`
- `tcp_client.display.windowCreate(name, width, height)`
- `tcp_client.display.windowRemove(name)`
- `tcp_client.display.windowMove(name, x, y)`
- `tcp_client.display.windowResize(name, width, height)`
- `tcp_client.display.windowVisibility(name, [visible])` (note that I'm not sure what this function does, and it might try to return some data and fail doing so)
- `tcp_client.display.windowShow(name)`
- `tcp_client.display.windowHide(name)`
- `tcp_client.display.windowFoxus(name)`

The other functions request data from the badge, and that functionality is not yet supported.

##### The RGB library
```
tcp_client.rgb.clear() #clears the screen such as you would do on the CZ19 badge with rgb.clear()
```

All other [methods](https://wiki.badge.team/Cz19#Display) work similarly, but `rgb.getbrightness()` and `rgb.textwidth()` have not yet been implemented.

##### Send raw data
```
tcp_client.send_packaged_data(p_data, data_descriptor)

p_data: packaged data, using the python struct library, with format data_descriptor.
data_descriptor: format of which data is packaged.
```

Check [structs](https://docs.python.org/3.5/library/struct.html#format-characters).

#### CZ19 badge
##### Initializing the server
```
tcp_server = tcpserver.CZ19_TCP_Server()
tcp_server.start()
```

If you want to add your own package handles, so that you can unpack your packages send in `tcp_client.send_packaged_data(p_data, data_descriptor)`, you can fill it as an argument to the start method:
```
tcp_server.start(package_handler)
```

The package handler should be defined as following:
```
def package_handler(packaged_data, descriptor)
```

Where you can easily decrypt the data with
```
data = struct.unpack(descriptor, packaged_data)
```
and do with it what you want.

##### Starting the server
```
tcp_server.start(package_handler, port=1234)
```

The server handles the `display` and `rgb` libraries by itself.
Default `port` is `1234`, assign variable to overwrite listening port.

## Demos
### Hello world
For the CZ19 badge, just start the tcplib-app.

On the CZ20Badge, create a new file for your `hello world` app with:
```
# Import your usual libraries
import keypad

# Import the cz1920_tcplib for the CZ20 badge
import apps.cz1920_tcplib

# Write the on_key handle
def on_key(key_index, is_pressed):
    if is_pressed: # only activate if the key is going down
        global tcp # get the tcp variable from outside this method
        tcp.send_int32(key_index) # send the current key pressed, as number to be displayed

# Load the TCP Library, this will also initialize wifi it is not yet connected
tcp = apps.cz1920_tcplib.CZ20_TCP_Client()
# Give the client the address and port to connect to
tcp.connect(host="<CZ19 Badge IP Address>", port=1234)

# Add the handler to the keypad
keypad.add_handler(on_key)

# Send "Hello World" to be displayed
tcp.send_text("Hello World!")
```

Where you replace `<CZ19 Badge IP Address>` with its IP. If you want to you can of course change the port as well, but you will have to match it with the port on the CZ19 badge.

Start the CZ20 Hello world app. If the system does not seem to work, check the known issues down below

## TODO
- [x] Create TCP Server for CZ19
- [x] Extract to seperate importable packages / libraries
- [x] Send structs over
- [x] Let CZ20 draw on CZ19 with direct `CZ19.rgb.<function>` handles
- [x] Let CZ20 draw on CZ19 with direct `CZ19.display.<function>` handles
- [ ] Let CZ19 talk back to CZ20
- [x] Write Hello World tutorial
- [ ] Write tutorial on how to use the structs
- [ ] Make the rgb and display library robust (throw correct errors when the wrong data is given)

## Known issues
Terminology:
- __Client__: CZ20 Badge running the CZ20_TCP_Client software
- __Server__: CZ19 Badge running the CZ19_TCP_Server software

| Issue | Reason | Potential fix |
|-------|--------|---------------|
| The client crashes on startup | The client can not find a server | First start the server app, then start the client app |
| The server does not respond to reconnections | The server still believes it is trying to connect to the "old" client | Restart the server |
| The serial tty from the server closes when waiting for IP | Global disasters, aliens, the mainframe being hacked, Campzone has become mudzone again (probably because of a time.sleep_ms call) | Re-open the serial tty |
