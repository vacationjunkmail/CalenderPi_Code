#!/usr/bin/env python3

import socket
import time

headersize = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
queue = 5

s.bind((socket.gethostname(),port))
s.listen(queue)

while True:
	clientsocket,address = s.accept()
	print(f"Connection from { address } has been established.")

	msg = "Welcome to the Server!"
	msg = f"{len(msg):<{headersize}}"+msg
	clientsocket.send(bytes(msg,"utf-8"))

	while True:
		time.sleep(3)
		msg = f"The time is {time.time()}"
		msg = f"{len(msg):<{headersize}}"+msg
		print(msg)
		clientsocket.send(bytes(msg,"utf-8"))
	#clientsocket.close()
	
