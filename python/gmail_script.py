#!/usr/bin/env python3
import configparser
from os.path import expanduser
from pathlib import Path

#https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
#http://www.vineetdhanawat.com/blog/2012/06/how-to-extract-email-gmail-contents-as-text-using-imaplib-via-imap-in-python-3/
#help from og pi http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
import smtplib
import datetime
import imaplib
import email
import sys
import os

dt_now = datetime.datetime.now()
home_path = expanduser("~")
home_path = str(Path.home())
filename = "{}/Downloads/{}_twitter.txt".format(home_path,dt_now.strftime('%a_%b_%d_%Y_%H_%M_%S_%p'))
print(filename)
sys.exit(1)

def read_config_file(filename='.config.ini', section='gmail'):

    parser = configparser.ConfigParser()
    config_file = "/home/pi/{}".format(filename)
    parser.read(config_file, encoding="utf-8")

    data = {}

    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        raise Exception("{0} not found in {1}".format(section, config_file))
    return data


class Gmail:
	def __init__(self,source_email):
		self.login_data = read_config_file()
		self.source_email = source_email
		self.delete_list = ['redditmail.com','shutterstock.com','target.com','moviesanywhere.com','sales.bogertmfg']
		self.delete_list.append('stackoverflow.email')
		self.delete_list.append('citadines.com')
		self.mail = ''
		self.download = '/home/pi/Downloads/temp/'
		self.menu = "/home/pi/Downloads/{}_menu.txt".format(dt_now.strftime('%a_%b_%d_%Y_%H_%M_%S_%p'))
		
	def login(self):
		
		self.mail = imaplib.IMAP4_SSL(self.login_data['server'])
		self.mail.login(self.login_data['address'],self.login_data['password'])
		self.mail.select('Inbox')

		return 'logged in'

	def delete(self):
		for item in self.delete_list:
			result, data = self.mail.uid('search', None, '(FROM "{}")'.format(item))
			i = len(data[0].split())
			#print track deleted emails
			files_deleted=0
			with open(self.source_email,'a+') as f:
				f.write("{}\n".format(datetime.datetime.now()))
			for x in range(i):
				files_deleted=files_deleted+1
				latest_email_uid = data[0].split()[x] # unique ids wrt label selected
				result, email_data = self.mail.uid('fetch', latest_email_uid, '(RFC822)')
				raw_email = email_data[0][1]
				raw_email_string = raw_email.decode('utf-8')
				email_message = email.message_from_string(raw_email_string)
				with open(self.source_email,'a+') as f:
					f.write("\tDate {}\n\tSubject {}\n\tFrom {}\n".format(email_message['date'],email_message['Subject'],email_message['FROM']))
				#delete email.
				delete_id = latest_email_uid.decode('utf-8')
				self.mail.uid('STORE',delete_id,'+FLAGS','\Deleted')
			file_title = "File"
			if files_deleted == 0 or files_deleted > 1:
				file_title = "Files"
			with open(self.source_email,'a+') as f:
				f.write("{} {} deleted from {}.\n\n".format(files_deleted,file_title,item))
			
		return 'Deleted Data'

	def attachment(self):
		#https://codereview.stackexchange.com/questions/190035/python-use-imap-lib-to-download-attachments-and-email-details
		#https://medium.com/@sdoshi579/to-read-emails-and-download-attachments-in-python-6d7d6b60269
		result, data = self.mail.uid('search', None, 'ALL')
		i = len(data[0].split())
		for x in range(i):
			latest_email_uid = data[0].split()[x]
			result, email_data = self.mail.uid('fetch', latest_email_uid, '(RFC822)')
			raw_email = email_data[0][1]

			raw_email_string = raw_email.decode('utf-8')
			email_message = email.message_from_string(raw_email_string)
			
			for part in email_message.walk():
				if part.get('Content-Disposition') != None:
					#print("x = {} maintype = {} cd = {}\n\tsubject = {}\n".format(x,part.get_content_maintype(),part.get('Content-Disposition'),email_message['subject']))
					my_file = part.get_filename()
					if bool(my_file):
						filePath = os.path.join(self.download, my_file)
						if not os.path.isfile(filePath):
							fp = open(filePath, 'wb')
							fp.write(part.get_payload(decode=True))
							fp.close()
							print("{} Download Complete.".format(filePath))

		return "Attachment"

	def weeklypost(self,subject="Weekly Menu"):
		result, data = self.mail.uid('search', None, '(HEADER Subject "{}")'.format(subject))
		#result, data = self.mail.uid('search', None, '(HEADER Subject "Weekly Post")')
		i = len(data[0].split())
		download_count = 0
		print(subject)
		for x in range(i):
			latest_email_uid = data[0].split()[x]
			result, email_data = self.mail.uid('fetch', latest_email_uid, '(RFC822)')
			raw_email = email_data[0][1]

			raw_email_string = raw_email.decode('utf-8')
			email_message = email.message_from_string(raw_email_string)
			for part in email_message.walk():
				if part.get_content_type() == 'text/plain':
					body = part.get_payload(decode=True)
					body = body.decode('utf-8').replace("\n","").strip().split("\r")
					for item in body:
						if len(item)<=140:
							download_count+=1
							if subject.lower() == 'weekly post':
								with open(filename,'a+') as f:
									f.write("{}\n".format(item))
							if subject.lower() == "weekly menu":
								with open(self.menu,'a+') as f:
									f.write("{}\n".format(item))
			delete_id = latest_email_uid.decode('utf-8')
			self.mail.uid('STORE',delete_id,'+FLAGS','\Deleted')
		if download_count > 0 and subject.lower() == 'weekly post':
			with open(filename,'a+') as f:
				f.write("Finish with news from {}\n".format(dt_now.strftime('%a %b %d %Y %H:%M:%S%p')))
		return_msg='{} {} Downloaded.'.format(download_count,subject)
		return return_msg

	def logout(self):
		self.mail.close()
		self.mail.logout()
		return "Goodbye : )"

a = Gmail('/home/pi/Desktop/deleted_target_email.log')
a.login()
#a.attachment()
print(a.weeklypost('Weekly Post'))
print(a.weeklypost('Weekly Menu'))
a.delete()
print(a.logout())
