"""
Test module for module customContainers
"""


import os
import sys
import unittest
if __name__ == '__main__': 
  sys.path.append( os.path.abspath('./../../') )
  os.chdir('./../../')
from gameobj.customContainers import *


class test_compactMatrix(unittest.TestCase):
  """Test class for compactMatrix"""
  def test_getitem(self):
    testobj = compactMatrix({'a': 1, 'b': 2, 'c': 3})
    self.assertEqual(testobj['a'], 1)
    self.assertEqual(testobj['b'], 2)
    self.assertEqual(testobj['d'], None)


class test_compactValueDict(unittest.TestCase):
  """Test class for compactValueDict"""
  def test_getitem(self):
    testobj = compactValueDict({'a': 1, 'b': 2, 'c': 3})
    self.assertEqual(testobj['a'], 1)
    self.assertEqual(testobj['b'], 2)
    self.assertEqual(testobj['d'], None)

  def test_multipop(self):
    testobj = compactValueDict({'a': 1, 'b': 2, 'c': 3, 'd': 1, 'e': 4})
    testobj._multiPop(['a', 'b', 'c'])
    self.assertEqual(testobj['a'], None)
    self.assertEqual(testobj['b'], None)
    self.assertEqual(testobj['c'], None)
    self.assertEqual(testobj['d'], 1)
    self.assertEqual(testobj['e'], 4)

  def test_convertFrom(self):
    testobj = compactValueDict({'a': 1, 'b': 2, 'c': 3, 'd': 3, 'e': 3})
    a = testobj.convertFrom(testobj)
    self.assertEqual(a, {'a': 1, 'b': 2, 'c': 3, 'd': 3, 'e': 3})
  
  def test_convertTo(self):
    testobj = compactValueDict.convertTo({'a': 1, 'b': 2, 'c': 3, 'd': 3, 'e': 3})
    for _, v in testobj.items(): v.sort()
    self.assertEqual(testobj, {1: ['a'], 2: ['b'], 3: ['c', 'd', 'e']})

  def test_pop(self):
    testobj = compactValueDict({'a': 1, 'b': 2, 'c': 3, 'd': 3, 'e': 3})
    self.assertEqual(testobj['e'], 3)
    self.assertEqual(testobj['c'], 3)
    testobj.pop('e')
    testobj.pop('c')
    self.assertEqual(testobj['e'], None)
    self.assertEqual(testobj['c'], None)

  def test_remove(self):
    testobj = compactValueDict({'a': 1, 'b': 2, 'c': 3, 'd': 3, 'e': 3})
    testobj.remove(3)
    self.assertEqual(testobj['a'], 1)
    self.assertEqual(testobj['b'], 2)
    self.assertEqual(testobj['c'], None)
    self.assertEqual(testobj['d'], None)
    self.assertEqual(testobj['e'], None)

  def test_update(self):
    testobj = compactValueDict({'a': 1, 'b': 2, 'c': 3, 'd': 3, 'e': 3})
    testobj.update({'f': 4, 'a': 2})
    self.assertEqual(testobj['a'], 2)
    self.assertEqual(testobj['f'], 4)


def starting_test():
  tb_line = 70 * '-'
  midline = '|' + (27 * ' ') + ('Starting Test') + (28 * ' ') + '|'
  print '\n'.join([tb_line, midline,tb_line])


def main():
  starting_test()
  unittest.TextTestRunner(verbosity=2).run(alltests)


compactMatrix_tests = unittest.TestLoader().loadTestsFromTestCase(test_compactMatrix)
compactValueDict_tests = unittest.TestLoader().loadTestsFromTestCase(test_compactValueDict)
alltests = unittest.TestSuite([
  compactMatrix_tests, 
  compactValueDict_tests,
])


if __name__ == '__main__':
  main()