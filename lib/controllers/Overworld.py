"""Game overworld stuff"""

import os, sys

if __name__ == '__main__':
  sys.path.append( os.path.abspath('./../') )
  os.chdir('./../')

from gameobj.board import MapArea
from gameobj.entities import EntityOverworld
from gui.guiMain import Gui
from mixins.CoordPos import AxisDistance, Coordinate, Direction


class Overworld(object):
  """docstring"""
  def __init__(self):
    self.gui = Gui()



