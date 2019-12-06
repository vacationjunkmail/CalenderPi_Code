#!/usr/bin/env python3

#/usr/local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#https://stackoverflow.com/questions/247770/how-to-retrieve-a-modules-path
#vi /home/pi/.local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#in_transaction
#https://overiq.com/mysql-connector-python-101/handling-transactions-with-connector-python/
import os, datetime, re, sys, time
from mysql_conn.connect_mysql import get_connection

#select_statement = '''select id,name from games.video_games where id= 1;'''
console_id = 13
select_statement = '''select v.id,v.`name`,g.console_shortname 
			from games.video_games as v inner join games.game_console as g on g.id=v.console_id 
			where g.id = {} and (v.small_image ='' or v.large_image = '' or v.small_image is null or v.large_image is null
			);'''.format(console_id)
select_consoles = 'select console_shortname from games.game_console where id = {};'.format(console_id)
update_query = ''' update games.video_games set large_image=%s, small_image=%s,header_image=%s where id = %s;'''
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

#path = '/var/www/blue_print_app/static/images'
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
			files = [f for f in os.listdir(search_path)]# if f.endswith('.txt')]
		except Exception as e:
			files = []
		if len(files):
			d[parent_dir][item]=files
for row in video_game_data:
	params = []
	if isinstance(row[1], bytes):
		image = row[1].decode().lower()
		system = row[2].decode()
	image = image.replace(' ','')
	regex = re.compile(r'^{}'.format(image),re.IGNORECASE)
	regex_match = re.compile(r'{}'.format(image),re.IGNORECASE)
	small = [f for f in d[system]['small'] if regex.search(f)]
	large = [f for f in d[system]['large'] if regex.search(f)]
	header = [f for f in d[system]['header'] if regex.search(f)]
	
	params2 = []

	for item in sub_dir:
		l1 = [f for f in d[system][item] if regex.search(f)]
		if len(l1)>1:
			l2 = remove_ext(l1)
			a = [f for f in l2 if regex_match.fullmatch(f)]
			if len(a):
				l1 = [l1[l2.index(a[0])]]
		if len(l1)>0:
			params2.append(l1[0])
		else:
			params2.append("NULL")

	s = ''
	l = ''
	h = ''
	if len(small):
		s = small[0]

	if len(large):
		l = large[0]

	if len(header):
		h = header[0]

	if len(small) == 0 and len(large) == 0 and len(header):
		continue
			
	params = [l,s,h,row[0]]
	params2.append(row[0])
	#print(params)
	print("Updating data for {}".format(row[1]))
	print(params2)
	mysql_db = get_connection()
	mysql_db.update_statement(update_query,params2)
	mysql_db.close_connection()

