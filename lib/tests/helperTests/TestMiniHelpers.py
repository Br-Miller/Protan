"""
Test module for module miniHelpers
"""


import os
import sys
import unittest
if __name__ == '__main__': sys.path.append( os.path.abspath('./../../lib') )
from helpers.miniHelpers import *


class test_miniHelpers(unittest.TestCase):
  """Test class for flatten"""
  def test_flatten(self):
    a = flatten([[1,2], 3, 4, 5, [6, 7, [8, 9]]])
    self.assertEqual(a, range(1, 10))
    a = flatten([1,[2,[3,[4,[5,[6,[7,[8,[9]]]]]]]]])
    self.assertEqual(a, range(1, 10))
    

def starting_test():
  tb_line = 70 * '-'
  midline = '|' + (27 * ' ') + ('Starting Test') + (28 * ' ') + '|'
  print '\n'.join([tb_line, midline,tb_line])


def main():
  starting_test()
  unittest.TextTestRunner(verbosity=2).run(alltests)


miniHelpers_tests = unittest.TestLoader().loadTestsFromTestCase(test_miniHelpers)
alltests = unittest.TestSuite([miniHelpers_tests])


if __name__ == '__main__':
  main()