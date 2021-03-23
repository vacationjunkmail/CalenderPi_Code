#!/usr/bin/env python3

import unittest
from unittest import mock
import io
from even import CheckList


expect = [6,48,36]
class TestEven(unittest.TestCase):
	def setUp(self):
		self.chk = CheckList([5,41,3,18,6,11,48,44,36])

	def test_verify_list(self):
		self.assertEqual(self.chk.verify_list(),[5,41,3,18,6,11,48,44,36])
		

	def test_verify_data(self):
		self.assertEqual(self.chk.verify_data(),9)

	def test_get_even(self):
		self.assertEqual(self.chk.get_even(),expect)

if __name__ == '__main__':
	unittest.main()
