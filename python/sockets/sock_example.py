#!/usr/bin/env python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server='oceancolor.gsfc.nasa.gov'
request = f"GET / HTTP/1.1\nHost: { server }\n\n"
request = "GET / HTTP/1.1\nHost: "+ server +"\n\n"
port = 80
#server_ip = socket.gethostbyname(server)
s.connect((server,port))
s.send(request.encode())
result = s.recv(4096)
while (len(result) > 0):
	print(result)
	result = s.recv(4096)
	
