#!/usr/bin/env python3

import socket
import pickle
from time import sleep
from sock_function import sock_var

v = sock_var()
headersize = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
length = 16
s.connect((socket.gethostname(),v['port']))

while True:
	full_msg = b''
	new_msg = True
	while True:
		msg = s.recv(v['length'])
		if new_msg:
			print(f"new msg len: {msg[:v['headersize']]}")
			msglen = int(msg[:v['headersize']])
			new_msg = False

		print(f"Full Message length: {msglen}")
		full_msg += msg
		print(len(full_msg))
		print(f"msglen:{msglen}")
		print(f"{len(full_msg) - 5}")
	if len(full_msg)-v['headersize'] == msglen:
		print(f"full msg recvd:")
		print(f"{full_msg[v['headersize']:]}")
		print(pickle.loads(full_msg[v['headersize']:]))
		new_msg = True
		full_msg = b''


