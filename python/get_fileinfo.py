#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  get_fileinfo.py
#
#  Copyright 2019  <pi@raspberrypi>
#logger.debug('debug message')
#logger.info('info message')
#logger.warning('warn message')
#logger.error('error message')
#logger.critical('critical message')

import exifread
import os
import logging
from logging.handlers import RotatingFileHandler
#[%(lineno)d]
logging.basicConfig(filename='get_file_info.log',format='%(levelname)s::%(name)s.%(funcName)s::%(asctime)s::%(message)s',level=20, datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('get_fileinfo')
#handler = RotatingFileHandler("my_log.log", maxBytes=2000, backupCount=10)
handler = RotatingFileHandler("get_file_info.log", maxBytes=132590, backupCount=2)
logger.addHandler(handler)

def main():
	#https://pypi.org/project/ExifRead/
	try:
		f = open('/home/pi/Downloads/temp/IMG_0137.JPG','rb')
		logger.info("Opening {}".format(f))
		tags = exifread.process_file(f,details=False)

		for item in tags:
			print("----{}:\t{}".format(item,tags[item]))

	except Exception as e:
		logger.warning(e)
	return 0

if __name__ == '__main__':
	main()
