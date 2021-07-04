#!/usr/bin/env python3

import socket
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
length = 8
s.connect((socket.gethostname(),port))

while True:
	full_msg = ''
	while True:
		msg = s.recv(length)
		if len(msg) <= 0:
			break
		full_msg += msg.decode("utf-8")

	if len(full_msg) > 0:
		print(full_msg)
