#!/usr/bin/env python3
#import imaplib, email, os
from gmail_setup import Gmail
#import gmail_setup

import os

def file_exist(f):
	#check if file exists
	file_status = os.path.exists(f)
	return file_status

source_email = '/home/pi/Desktop/email.log'

#source_exists = os.path.exists(source_email)

source_exists = file_exist(source_email)

if source_exists:
	os.remove(source_email)
	
a = Gmail(source_email)

a.login()
a.logout()

final_email = '/home/pi/Desktop/email.txt'

#exists = os.path.exists(final_email)

destination_exists = file_exist(final_email)
if destination_exists:
	os.remove(final_email)

source_exists = file_exist(source_email)

if source_exists:
	c = 0
	with open(source_email) as f:
		for line in f:
			#line = trim(line)
			line = line.strip('\n')
			if len(line) > 0:
				with open(final_email,'a+') as n:
					if c == 0:
						n.write(line)
					else:
						line = "\n{}".format(line)
						n.write(line)
			c += 1
	
#print(lines)
