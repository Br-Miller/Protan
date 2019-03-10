"""
Test module for module CoordPos
"""


import os
import sys
import unittest
if __name__ == '__main__': sys.path.append( os.path.abspath('./../../../lib') )
from mixins.CoordPos import *


class test_AxisDistance(unittest.TestCase):
  """Test
  Not yet completed
  """
  def setUp(self):
    self.objA = AxisDistance(sx=1)
    self.objB = AxisDistance(px=1)
    self.objC = AxisDistance(t=1)
    self.objD = AxisDistance(px=31, sx=8)
    self.objE = AxisDistance(px=16, sx=4)

  def test_ClassVars(self):
    self.assertEqual(AxisDistance.tilesize, 32)
    self.assertEqual(AxisDistance.pixelsize, 8)

  def test_cleanup(AxisDistance):
    self.assertEqual(self.objD.tile, 1)
    self.assertEqual(self.objD.tile, 0)
    self.assertEqual(self.objD.tile, 0)

  def test_iter(self):
    self.assertEqual(tuple(self.objA), (0, 0, 1))
    self.assertEqual(tuple(self.objB), (0, 1, 0))
    self.assertEqual(tuple(self.objC), (1, 0, 0))

  def test_str(self):
    self.assertEqual(str(self.objA), '0.0.1')
    self.assertEqual(str(self.objB), '0.1.0')
    self.assertEqual(str(self.objC), '1.0.0')

  def test_add(self):
    self.assertEqual(self.objE + self.objE, AxisDistance(t=1,px=1))


class test_Coordinate(unittest.TestCase):
  """Out of date"""
  def setUp(self):
    self.coorda = Coordinate(0, 0)
    self.coordb = Coordinate(2, 7)
    self.coordc = Coordinate(5, 2)
    self.coordd = Coordinate(5, 5)

  def test_shift(self):
    d = {
      self.coorda + self.coordb: ( 2, 7),
      self.coordb + self.coordc: ( 7, 9),
      self.coordb - self.coordc: (-3, 5),
    }
    for k, v in d.items():
      self.assertEqual((k.x, k.y), v)

  def test_shiftDir(self):
    d = {
      self.coorda.shiftDir(0): ( 0,  1),
      self.coorda.shiftDir(1): ( 1,  1),
      self.coorda.shiftDir(2): ( 1,  0),
      self.coorda.shiftDir(3): ( 1, -1),
      self.coorda.shiftDir(4): ( 0, -1),
      self.coorda.shiftDir(5): (-1, -1),
      self.coorda.shiftDir(6): (-1,  0),
      self.coorda.shiftDir(7): (-1,  1),
      self.coorda.shiftDir(8): ( 0,  0),
    }
    for k, v in d.items():
      self.assertEqual((k.x, k.y), v)

  def test_distTo(self):
    da = {
      self.coorda.distTo(self.coordb, total=True): 9,
      self.coordb.distTo(self.coordc, total=True): 8,
      self.coordc.distTo(self.coordd, total=True): 3,
    }
    db = {
      self.coorda.distTo(self.coordb, total=False): ( 2,  7),
      self.coordb.distTo(self.coordc, total=False): ( 3, -5),
      self.coordc.distTo(self.coordd, total=False): ( 0,  3),
    }
    for k, v in da.items():
      self.assertEqual(k, v)

    for k, v in db.items():
      self.assertEqual((k.x, k.y), v)

  def test_inBounds(self):
      pass

  def test_flip(self):
    d = {
      self.coorda.flip(axis='x' ): ( 0,  0),
      self.coorda.flip(axis='y' ): ( 0,  0),
      self.coorda.flip(axis='xy'): ( 0,  0),
      self.coordb.flip(axis='x' ): (-2,  7),
      self.coordb.flip(axis='y' ): ( 2, -7),
      self.coordb.flip(axis='xy'): (-2, -7),
      self.coordc.flip(axis='x' ): (-5,  2),
      self.coordc.flip(axis='y' ): ( 5, -2),
      self.coordc.flip(axis='xy'): (-5, -2),
      self.coordd.flip(axis='x' ): (-5,  5),
      self.coordd.flip(axis='y' ): ( 5, -5),
      self.coordd.flip(axis='xy'): (-5, -5),
    }
    for k, v in d.items():
      self.assertEqual((k.x, k.y), v)




def starting_test():
  tb_line = 70 * '-'
  midline = '|' + (27 * ' ') + ('Starting Test') + (28 * ' ') + '|'
  print '\n'.join([tb_line, midline,tb_line])


Coordinate_test = unittest.TestLoader().loadTestsFromTestCase(test_Coordinate)
alltests = unittest.TestSuite([Coordinate_test])


if __name__ == '__main__':
  starting_test()
  unittest.TextTestRunner(verbosity=2).run(alltests)