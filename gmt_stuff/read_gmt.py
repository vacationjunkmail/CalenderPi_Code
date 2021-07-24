#!/usr/bin/env python3

import re

a_z = re.compile(r'[a-z]',re.IGNORECASE)

gmt_file = '/home/pi/Desktop/gmt_color.txt'

with open(gmt_file,'r+') as f:
	file_data = f.readlines()

for item in file_data:
	item = item.strip()
	if a_z.search(item):
		with open('/home/pi/Desktop/fixed_gmt_colors.txt','a+') as f:
			item = f'{item}\n'
			f.write(item)
