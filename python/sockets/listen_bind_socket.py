#!/usr/bin/env python3

import socket
import sys

host = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((host,port))
except socket.error as e:
	print(f"Bind failed: { e }")
	sys.exit()

s.listen(10)

conn, addr = s.accept()

print(f"Connected with { addr[0] }: { addr[1] }")
