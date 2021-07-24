#!/usr/bin/env python3

import socket
from time import sleep

headersize = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
length = 16
s.connect((socket.gethostname(),port))

while True:
	full_msg = ''
	new_msg = True
	while True:
		msg = s.recv(length)
		if new_msg:
			print(f"new msg len: {msg[:headersize]}")
			msglen = int(msg[:headersize])
			new_msg = False

		print(f"Full Message length: {msglen}")
		full_msg += msg.decode("utf-8")
		print(len(full_msg))

	if len(full_msg)-headersize == msglen:
		print(f"full msg recvd:\n{full_msg[headersize:]}")
		new_msg = True
		full_msg = ''


