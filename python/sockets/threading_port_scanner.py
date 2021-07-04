#!/usr/bin/env python3

import socket
import sys
import threading
from queue import Queue
import time

start = time.time()
print_lock = threading.Lock()

target = 'hackthissite.org'

def pscan(port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		conn = s.connect((target,port))
		with print_lock:
			print(f"port:{port}")
		conn.close()
	except Exception as e:
		print(e)
		pass

def threader():
	while True:
		worker = q.get()
		pscan(worker)
		q.task_done()

q = Queue()
		
for x in range(25):
	t = threading.Thread(target=threader)
	t.daemon = True
	t.start()


for worker in range(1,100):
	q.put(worker)

q.join()

stop = time.time()
print(f"start {start} stop {stop}")
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
