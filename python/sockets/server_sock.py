#!/usr/bin/env python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
queue = 5

s.bind((socket.gethostname(),port))
s.listen(queue)

while True:
	clientsocket,address = s.accept()
	print(f"Connection from { address } has been established.")
	clientsocket.send(bytes("Hey there!!! this is a very long message a lot of characters just to see if buffering really works\ttabs","utf-8"))
	clientsocket.close()
	
