#!/usr/bin/env python3

import os, datetime

path = '/home/pi/Desktop'
file_name = '{}/new_file.txt'.format(path)
t = datetime.datetime.now()
with open(file_name,'wt+') as f:
	f.write('Hello {}'.format(t));

