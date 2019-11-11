#!/usr/bin/env python3

import os, datetime, re, sys

file_name = ['/home/pi/Downloads/temp/bookmarks.html','/home/pi/Downloads/temp/RaspberryPiMusic.txt',
'/home/pi/Downloads/temp/GameYoutube.txt','/home/pi/Downloads/temp/GameWikipedia.txt',
'/home/pi/Downloads/temp/GameTitle.txt','/home/pi/Downloads/temp/GameFaqs.txt']

t = datetime.datetime.now()
complete_file = "/home/pi/Downloads/{}_twitter.txt".format(t.strftime('%a_%b_%d_%Y_%H_%M_%S_%p'))

hash_regex = re.compile(r'#',re.IGNORECASE)
dt_regex = re.compile(r'HREF',re.IGNORECASE)
capture_regex = re.compile(r'(?<=HREF=").*?(?=")',re.IGNORECASE)
capture_title = re.compile(r'(?<=">).*?(?=<)',re.IGNORECASE)
skip_regex = re.compile(r'place:',re.IGNORECASE)
#capture_regex_works = re.compile(r'(?<=HREF=")([^"]*)(?:")',re.IGNORECASE)
remove_list = ['ie=UTF8&','showViewpoints=0&','wa_user1=2&','wa_user2=History&',
'wa_user1=5&','wa_user2=Science&','wa_user3=article&','wa_user1=3&','wa_user4=recommended&',
'utm_source=theslingshot&','utm_medium=referral&','?utm_campaign=top-10-best-pro-wresting-games',
'wa_user4=recommended','&feature=related','&feature=channel','&feature=fvw','&feature=player_embedded',
'&feature=channel_page','plp.mpsomaha.org/','Wikipedia, the free encyclopedia']

skip_list = ['esu3','205.202.254.18','cfide','ralstonschools','weepingwater','ishareinfo',
'mpsomaha','lpslions','fortcalhoun','dcwest','Bennington','Elkhorn','forms.']

clean_hash = [":","_","'","(",")",".","!","-"]

skip_me_regex = []
for exp in skip_list:
	skip_me_regex.append(re.compile(r'{}'.format(exp),re.IGNORECASE))

def trim_link(f_link):
	trim_num=len(f_link)-140
	f_link = f_link[:-trim_num]
	return f_link

links_set = set()

for file in file_name:
	with open(file,'r+') as f:
		data=f.readlines()
	for line in data:
		line = line.strip()
		if any(regex.search(line) for regex in skip_me_regex):
			continue
		elif dt_regex.search(line) and not skip_regex.search(line):
			#m = capture_regex_works.findall(line)
			#print(m[0])
			link = capture_regex.search(line)
			title = capture_title.search(line)	
			combo = "{} {}".format(link.group(),title.group())
			for word in remove_list:
				combo = combo.replace(word,"")
			if len(combo) >140 and len(link.group()) <= 140:
				combo = trim_link(combo)
			elif len(combo)>140 and len(link.group())>140:
				combo = trim_link(combo)
			if len(combo)>0:
				#with open(complete_file,'a+') as f:
					#f.write("{}\n".format(combo))
				links_set.add(combo)
		elif file != '/home/pi/Downloads/temp/bookmarks.html':
			if len(line.strip())>0:
				if file =='/home/pi/Downloads/temp/GameTitle.txt':
					l = line
					line = line.replace(" ","")
					line = "{} #{} #ps2".format(l,line.lower())
				elif file=='/home/pi/Downloads/temp/GameWikipedia.txt':
					l = line
					line = line.split("/")
					line = line[-1]
					for item in clean_hash:
						line = line.replace(item,"")
					if hash_regex.search(line):
						line = line.replace("#","")

					line = "{} #{}".format(l,line)	

				links_set.add(line)
for link in links_set:
	with open(complete_file,'a+') as f:
		f.write("{}\n".format(link))
