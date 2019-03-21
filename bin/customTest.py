"""
Test, should be deleted
"""


import os, sys

sys.dont_write_bytecode = True
sys.path.append( os.path.abspath('./../lib') )
os.chdir('./../lib')

from gameobj.board import MapArea
from gameobj.entities import EntityOverworld
from mixins.CoordPos import AxisDistance, BasicRectangleArea, Coordinate, Direction
from gui.guiMain import Gui

gui = Gui()
gui('board.show', True)
entityA = EntityOverworld(Coordinate((0, 0, 0), (0, 0, 0)), {'name': 'amberSoldier', 'facing': 'n', 'moveSpeed': {'t': 0, 'px': 2, 'sx': 0}, 'customHitbox': None})
entityB = EntityOverworld(Coordinate((7, 0, 0), (7, 0, 0)), {'name': 'debug1', 'facing': 's', 'moveSpeed': {'t': 0, 'px': 2, 'sx': 0}, 'customHitbox': None})
board = MapArea(AxisDistance(t=30), AxisDistance(t=20), b='.debug1')
entities = [entityA, entityB]

def getInput():
  return raw_input('input direction: ')

def update():
  gui('board.update', True, board, entities)
  gui('update', True)

def mainA():
  while True:
    update()
    a = getInput()
    a = a.strip()
    if Direction.isDir(a):
      entityA.move(board, entities, face=a)

def main():
  for i in range(60):
    entityA.tick()
    entityB.tick()
    update()
  for i in range(224):
    entityA.tick()
    entityB.tick()
    entityA.move(board, entities, face='ne')
    update()


if __name__ == '__main__':
  main()
