#!/usr/bin/env python3

import os, datetime, sys, random

class CheckList:
	def __init__(self,lst):
		self.lst = lst
		self.log = '/tmp/even_log.log'
		self.msg = ''
		self.new_lst = []

	def verify_list(self):
		if not isinstance(self.lst,list):
			#not a list
			print("Error 1")
			self.msg = 'Error 1: {}\n'.format(type(self.lst))
			self.err_log()
			sys.exit()
		else:
			l = [self.raise_error(item) for item in self.lst ]
		return self.lst

	def raise_error(self,item):
		if not(isinstance(item,int)):
			print('Error 2')
			self.msg = 'Error 2: {}\n'.format(type(item))
			self.err_log()
			sys.exit()
		return True

	def err_log(self):
		with open(self.log,'a+') as f:
			f.write(self.msg)
		return

	def get_even(self):
		new_lst = self.lst[::2]
		self.new_lst = 	[item for item in new_lst if item % 2 == 0]	
		return [self.lst,self.new_lst]

my_list = random.sample(range(0,50),9)
l = CheckList(my_list)
l.verify_list()
results=l.get_even()

print("Original List:{}\nNew List:{}".format(results[0],results[1]))



