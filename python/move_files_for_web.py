#!/usr/bin/env python3

from mysql_conn.connect_mysql import get_connection

import shutil
import os

update_query = '''update games.video_games set small_image=%s, large_image=%s where id = %s;'''
query = '''select v.id,v.`name`,g.console_shortname,v.small_image,v.large_image 
	   from games.video_games as v inner join games.game_console as g on g.id=v.console_id 
	   where v.id in (177,180,176);'''
mysql_db = get_connection()

game_data = mysql_db.select_no_params(query)

mysql_db.close_connection()

base_dir = '/var/www/public/images'


def move_files(source,destination):
	#move
	#print(source,destination)
	shutil.move(source,destination)
	return ""

def update_videogame(params):
	mysql_db = get_connection()
	mysql_db.update_statement(update_query,params)
	mysql_db.close_connection()
	#print(s)
	return ""

for row in game_data[1]:
	print(row['name'])
	small_location = "{}/{}/small".format(base_dir,row['console_shortname'])
	large_location = "{}/{}/large".format(base_dir,row['console_shortname'])
	small_source = "{}/{}".format(small_location,row['small_image'])
	large_source = "{}/{}".format(large_location,row['large_image'])
	og_small_source = "{}/{}".format(base_dir,row['small_image'])
	if row['small_image'] == row['large_image']:
		#move small to base directory
		#small_source = "{}/{}".format(small_location,row['small_image'])
		move_files(small_source,base_dir)
		#move large to small
		#large_source = "{}/{}".format(large_location,row['large_image'])
		move_files(large_source,small_location)
		#move og small to large
		#og_small_source = "{}/{}".format(base_dir,row['small_image'])
		move_files(og_small_source,large_location)
	else:
		params = [row['large_image'],row['small_image'],row['id']]
		move_files(small_source,large_location)
		move_files(large_source,small_location)	
		update_videogame(params)
