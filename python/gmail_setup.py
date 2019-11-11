#!/usr/bin/env python3
import configparser
from os.path import expanduser

#https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
#http://www.vineetdhanawat.com/blog/2012/06/how-to-extract-email-gmail-contents-as-text-using-imaplib-via-imap-in-python-3/

import smtplib
import time
import imaplib
import email

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
		
	def login(self):
		
		mail = imaplib.IMAP4_SSL(self.login_data['server'])
		mail.login(self.login_data['address'],self.login_data['password'])
		
		mail.select('Inbox')
		
		result, data = mail.uid('search', None, '(HEADER Subject "Weekly Post")')
		
		i = len(data[0].split())
		
		for x in range(i):
			latest_email_uid = data[0].split()[x] # unique ids wrt label selected
			result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
			raw_email = email_data[0][1]
			
			raw_email_string = raw_email.decode('utf-8')
			
			email_message = email.message_from_string(raw_email_string)
			print(email_message['Subject'])
			for part in email_message.walk():				
				if part.get_content_type() == "text/plain":
					body = part.get_payload(decode=True)
					body = body.decode('utf-8')

					with open(self.source_email,'a+') as f:
						f.write(body)	
					
					#delete email.
			delete_id = latest_email_uid.decode('utf-8')
			mail.uid('STORE',delete_id,'+FLAGS','\Deleted')
			print(self.source_email,delete_id)									
			#mail.store("1:{}".format(delete_id), '+X-GM-LABELS', '\Trash')
			#mail.store(delete_id, '+FLAGS', '\\Trash')
			#mail.store(delete_id, '+FLAGS', '\\Deleted')
			#mail.store("{}".format(delete_id), '+X-GM-LABELS', '\\Trash')
			#mail.expunge()
		mail.close()
		mail.logout()
		return 'logged in'
	
	def logout(self):
		return("Goodbye : )")
