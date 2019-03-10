"""
This module runs all the tests at once
"""


import os
import sys
import unittest
if __name__ == '__main__': 
  sys.path.append( os.path.abspath('./../') )
  os.chdir('./../')
from mixinTests import *
from helperTests import *
from gameobjTests import *


def isTest(s):
  assert isinstance(s, str), "incorrect type of arg s: should be type str, is type {}".format(type(s))
  return s[:4] == 'Test'


def getAllTests():
  alltests = []
  for k, v in globals().items():
    if isTest(k):
      alltests.extend(v.alltests)
  return alltests


def starting_test():
  tb_line = 70 * '-'
  midline = '|' + (27 * ' ') + ('Starting Test') + (28 * ' ') + '|'
  print '\n'.join([tb_line, midline, tb_line])


def main(verbosity=1):
  starting_test()
  tests = unittest.TestSuite(getAllTests())
  unittest.TextTestRunner(verbosity=verbosity).run(tests)


if __name__ == '__main__':
  main(2)