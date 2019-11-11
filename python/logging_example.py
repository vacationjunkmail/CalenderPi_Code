#!/usr/bin/env python3

import logging
from datetime import date

logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.debug('This is the debug message')
logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything
print(date.now())

