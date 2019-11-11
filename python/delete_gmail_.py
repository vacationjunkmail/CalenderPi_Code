#!/usr/bin/env python3
import configparser
from os.path import expanduser

#https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
#http://www.vineetdhanawat.com/blog/2012/06/how-to-extract-email-gmail-contents-as-text-using-imaplib-via-imap-in-python-3/

import smtplib
import datetime
import imaplib
import email
import sys

def read_config_file(filename = '.config.ini', section = 'gmail'):
    parser = configparser.ConfigParser()
    config_file = "{}/{}".format(expanduser("~"),filename)
    parser.read(config_file,encoding = "utf-8")

    data = {}
    
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        raise Exception("{0} not found in {1}".format(section,config_file))
    return data


class Gmail:
	def __init__(self,source_email):
		self.login_data = read_config_file()
		self.source_email = source_email
		self.delete_list = ['redditmail.com','shutterstock.com','target.com','moviesanywhere.com','sales.bogertmfg']
		self.delete_list.append('stackoverflow.email')
		self.delete_list.append('citadines.com')
		
	def login(self):
		
		mail = imaplib.IMAP4_SSL(self.login_data['server'])
		mail.login(self.login_data['address'],self.login_data['password'])
		
		mail.select('Inbox')

		for item in self.delete_list:
			#result, data = mail.uid('search', None, '(HEADER FROM "target.com")')
			#result, data = mail.uid('search', None, '(FROM "redditmail.com")')
			result, data = mail.uid('search', None, '(FROM "{}")'.format(item))
		
			i = len(data[0].split())
			#print track deleted emails
			files_deleted=0
			with open(self.source_email,'a+') as f:
				f.write("{}\n".format(datetime.datetime.now()))	
			for x in range(i):
				files_deleted=files_deleted+1
				latest_email_uid = data[0].split()[x] # unique ids wrt label selected
				result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
				raw_email = email_data[0][1]
			
				raw_email_string = raw_email.decode('utf-8')
				email_message = email.message_from_string(raw_email_string)
				with open(self.source_email,'a+') as f:
					f.write("\tDate {}\n\tSubject {}\n\tFrom {}\n".format(email_message['date'],email_message['Subject'],email_message['FROM']))
					
				#delete email.
				delete_id = latest_email_uid.decode('utf-8')
				mail.uid('STORE',delete_id,'+FLAGS','\Deleted')

			file_title = "File"
			if files_deleted == 0 or files_deleted > 1:
				file_title = "Files"
			with open(self.source_email,'a+') as f:
				f.write("{} {} deleted from {}.\n\n".format(files_deleted,file_title,item))

		mail.close()
		mail.logout()
		return 'logged in'
	
	def logout(self):
		return("Goodbye : )")

a = Gmail('/home/pi/Desktop/deleted_target_email.log')
a.login()
a.logout()
