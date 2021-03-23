#!/usr/bin/env python3

import os, datetime, sys, random

class CheckList:
	def __init__(self,lst):
		self.lst = lst
		self.new_lst = []
		self.err_file = '/tmp/checklst.log'
		self.msg = ''

	def verify_list(self):
		if not isinstance(self.lst,list):
			self.msg = 'Error 1: {}\n'.format(type(self.lst))
			self.err_log()
			raise TypeError('Not type list')
			sys.exit()
		return self.lst

	def verify_data(self):
		l = [item for item in self.lst if isinstance(item,int)]
		return len(l)

	def get_even(self):
		new_lst = self.lst[::2]
		self.new_lst = 	[item for item in new_lst if item % 2 == 0]	
		return self.new_lst
	
	def err_log(self):
		with open(self.err_file,'a+') as f:
			f.write(self.msg)
		return 

