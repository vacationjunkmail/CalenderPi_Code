#!/usr/bin/env python3

#/usr/local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#https://stackoverflow.com/questions/247770/how-to-retrieve-a-modules-path
#vi /home/pi/.local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#in_transaction
#https://overiq.com/mysql-connector-python-101/handling-transactions-with-connector-python/
import os, datetime, re, sys, time
from mysql_conn.connect_mysql import get_connection

console_id = 4
select_statement = '''select v.id,v.`name`,g.console_shortname 
			from games.video_games as v inner join games.game_console as g on g.id=v.console_id 
			where g.id = {} and (v.small_image ='' or v.large_image = '' or v.small_image is null or v.large_image is null
			or header_image is null or header_image = '');'''.format(console_id)

select_consoles = 'select console_shortname from games.game_console where id = {};'.format(console_id)
update_query = ''' update games.video_games set small_image=%s, large_image=%s,header_image=%s where id = %s;'''
def stop_me():
	print("Planned exit Program did not finish!")
	sys.exit()
	return ''

def remove_ext(l):
	new_list = []
	for item in l:
		new_list.append(item.split(".")[0])
	return new_list

script_name = os.path.abspath(__file__)

path = '/var/www/public/images'

mysql_db = get_connection()
video_game_query = mysql_db.select_query(select_statement)
video_game_data = video_game_query.fetchall()
mysql_db.close_connection()

mysql_db = get_connection()
console_query = mysql_db.select_query(select_consoles)
console_data = console_query.fetchall()
mysql_db.close_connection()

sub_dir=['small','large','header']
nested_dict = {}
d = {}

for row in console_data:
	if isinstance(row[0], bytes):
		parent_dir = row[0].decode()
	d[parent_dir]={}
	for item in sub_dir:
		d[parent_dir][item] = []
		search_path = "{}/{}/{}".format(path,parent_dir,item)
		try:
			files = [f for f in os.listdir(search_path)]
		except Exception as e:
			files = []
		if len(files):
			d[parent_dir][item]=files

for row in video_game_data:
	if isinstance(row[1], bytes):
		image = row[1].decode().lower()
		system = row[2].decode()
	image = image.replace(' ','')
	regex = re.compile(r'^{}'.format(image),re.I)
	regex_match = re.compile(r'^{}$'.format(re.escape(image)),re.IGNORECASE)
	params2 = []

	for item in sub_dir:
		l1 = [f for f in d[system][item] if regex.search(f)]
		file = ''
		if len(l1):
			l2 = remove_ext(l1)
			a = [f for f in l2 if regex_match.search(f)]
			if len(a):
				file = l1[l2.index(a[0])]
		params2.append(file)

	params2.append(row[0])
	print("Updating data for {} id {}".format(row[1].decode(),row[0]))
	#print(params2)
	mysql_db = get_connection()
	mysql_db.update_statement(update_query,params2)
	mysql_db.close_connection()

