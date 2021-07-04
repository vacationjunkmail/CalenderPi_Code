#!/usr/bin/env python3

import socket
import ssl
import sys

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_default_certs()

server='oceancolor.gsfc.nasa.gov'
server='pythonprogramming.net'
port = 443
server_ip = socket.gethostbyname(server)
print(server_ip)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = context.wrap_socket(s, server_hostname=server)

request = f"GET / HTTP/1.1\nHost: { server }\n\n"
#request = "GET / HTTP/1.1\nHost: "+ server +"\n\n"
s.connect((server,port))
s.send(request.encode())
result = s.recv(4096)
while (len(result) > 0):
	print(result)
	result = s.recv(4096)
	
