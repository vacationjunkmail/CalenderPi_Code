#!/usr/bin/env python3

#/usr/local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#https://stackoverflow.com/questions/247770/how-to-retrieve-a-modules-path
#vi /home/pi/.local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#in_transaction
#https://overiq.com/mysql-connector-python-101/handling-transactions-with-connector-python/
import os, datetime, re, sys, time
from mysql_conn.connect_mysql import get_connection
import uuid

insert_query = '''insert into test_db.test_tbl_2(username,pwd)values(%s,%s);'''
insert_path =  '''insert into test_db.paths_tbl_2(user_id,path)values(%s,%s)'''
def stop_me():
	print("Planned exit Program did not finish!")
	sys.exit()
	return ''

error_msg = []
data_dict = {}
for i in range(1,6):
	pwd = uuid.uuid4().hex[:8]
	un = "username_{}".format(pwd[:4])
	insert_params = [un,i]
	path = "/{}/{}".format(un,pwd)
	path_params=[path]

	#if i > 2 and i < 4:
	#	insert_params.append("asdfafaffffffff")

	#works
	mysql_db = get_connection()
	try:
		mysql_db.conn.start_transaction()
		mysql_db.curr.execute(insert_query,insert_params)
		path_params.insert(0,mysql_db.curr.lastrowid)
		mysql_db.curr.execute(insert_path,path_params)
		data_dict[un] = [insert_query,insert_params]
		mysql_db.conn.commit()
	except Exception as e:
		mysql_db.conn.rollback()
		d = {un:e}
		error_msg.append(d)

	mysql_db.close_connection()

for key in data_dict:
	print(data_dict[key][0],data_dict[key][1])
	
if len(error_msg)>0:
	print("Rolling Back Some updates and inserts")
	for dict_item in error_msg:
		for key in dict_item:
			print("{}:{}".format(key,dict_item[key]))

