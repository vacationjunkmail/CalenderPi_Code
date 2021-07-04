#!/usr/bin/env python3

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target = input('What webstie to scan?')
def pscan(port):
	try:
		conn = s.connect((target,port))
		return True
	except Exception as e:
		print(e)
		return False
for x in range(25):
	if pscan(x):
		print(f"Port: { x } is open")

#server='oceancolor.gsfc.nasa.gov'
#request = f"GET / HTTP/1.1\nHost: { server }\n\n"
#request = "GET / HTTP/1.1\nHost: "+ server +"\n\n"
#port = 80
##server_ip = socket.gethostbyname(server)
#s.connect((server,port))
#s.send(request.encode())
#result = s.recv(4096)
#while (len(result) > 0):
#	print(result)
#	result = s.recv(4096)
#	
