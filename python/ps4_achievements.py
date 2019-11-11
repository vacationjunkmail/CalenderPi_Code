#!/usr/bin/env python3

import os, exifread, datetime
from contextlib import suppress

def convert_date(d):
	d = str(d).strip()
	d = datetime.datetime.strptime(d,'%Y:%m:%d %H:%M:%S')
	d = d.strftime('%A %B %d %Y %I:%M:%S %p')
	return d

name_len = 0
date_len = 0
file_len = 0

i = 1
loading = '.'

if __name__ == '__main__':

	directory = '/media/pi/BC59-4984/PS4/SHARE/Screenshots/'

	mysql_achievement = '/home/pi/Downloads/achievements.sql'

	file_list = [os.path.join(path, name) for path, subdirs, files in os.walk(directory) for name in files]

	with suppress(OSError):
		os.remove(mysql_achievement)

	with open(mysql_achievement,'w'):
		pass

	for file in file_list:
		#get_date = file.split("_")
		file_split = file.split("/")
		#get_date = get_date[-1].split(".")
		#get_date = get_date[0]
		game_name = file_split[7].replace("_","")	
		file_name = file_split[-1]
		f = open(file, 'rb')
		tags = exifread.process_file(f, details=False)
		date = {tag for (count, tag) in enumerate(tags) if tag == 'EXIF DateTimeDigitized'}
		date = next(iter(date))
		date = tags[date]
		date = convert_date(date)

		with open (mysql_achievement,'a') as f:
			f.write('insert into achievements.achievement(title,date,file_name) values("{}","{}","{}");\n'.format(game_name,date,file_name))

		if i % 50 == 1 and i > 1:
			#print("{} lines printed.".format(i))
			print(loading)
			loading+='.'

		i += 1

		if len(game_name) > name_len:
			name_len = len(game_name)

		if len(date) > date_len:
			date_len = len(date)

		if len(file_name) > file_len:
			file_len = len(file_name)
		#for a, b in enumerate(tags):
			#if b == 'JPEGThumbnail':
				#pass
			#else:
				#print(a,b,tags[b])
		#break
	print('Script is done')
