# CZ1920 TCPlib

A library to share data between the Campzone 2019 HackerZones and Campzone 2020 Hackerzone badges. 

## Usage
### Installation
- Install https://badge.team/projects/cz1920_tcplib on your CZ20 badge.
- Install on your CZ19 badge.
- Get the ip-address from your CZ19 badge and set this ip address to the `server_ip` in your CZ20 badge at [the webusb website](webusb.hackz.one/settings).

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
CZ20_TCP_Client.connect(host=None, port=None)
```

By giving any values to any of these parameters you will overwrite the previously set ones and the tcp server will connect to the new address.

(Note: if there is no server running on this connection, the client will crash trying to get a tcp connection up).

##### Stopping the client
```
CZ20_TCP_Client.stop()
```

##### Reconnecting the client
```
CZ20_TCP_Client.reconnect()
```

Todo: allow for new host and port settings

##### Send raw data
```
CZ20_TCP_Client.send_data(data, data_descriptor)

data: packaged data, using the python struct library, with format data_descriptor.
data_descriptor: format of which data is packaged.
```

Check [structs](https://docs.python.org/3.5/library/struct.html#format-characters).

##### Prebuild data handling
```
CZ20_TCP_Client.send_text(string)
CZ20_TCP_Client.send_int32(i)
CZ20_TCP_Client.send_float(f)
CZ20_TCP_Client.send_double(d)
```

#### CZ19 badge
##### Initializing the server
```
CZ20 = tcpserver.CZ19_TCP_Server()
CZ20.start(package_handler)
```

The `package_handler` is a handle that is able to unpack the data coming in. The current default handler is only able to unpack strings

##### Starting the server
```
CZ19_TCP_Server.start(callback, port=1234)
```

`callback` is a the handle described before, with parameters `p_data` and `descriptor`.
`p_data` is the packaged data, to be unpackaged and `descriptor` is the descriptor of how the data is formatted, also known as the format of the struct. If you know what the descriptor is, you can unpack the data accordingly.

In the future there will be some unpack-libraries (e.g. for the `CZ19.display` handles).

Default `port` is `1234`, assign variable to overwrite listening port.

## Demos
Still have to add some features before I will be making demos.

## TODO
- [x] Create TCP Server for CZ19
- [ ] Extract to seperate importable packages / libraries
- [ ] Send structs over
- [ ] Let CZ20 draw on CZ19 with direct `CZ19.display.<function>` handles
- [ ] Let CZ19 talk back to CZ20

### Known issues
- The client crashes if there is no server available
