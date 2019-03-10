"""Game Entity code

All time is measured in ticks (60TicksPerSecond)
All distance is measured in AxisDistance

Pending Updates
  Add customHitbox on Overworld Entity
"""

import os, sys
if __name__ == '__main__': 
  sys.path.append( os.path.abspath('./../') )
  os.chdir('./../')
from mixins.CoordPos import AxisDistance, BasicRectangleArea, Coordinate, Direction


TicksPerSecond = 60
TilePixels = AxisDistance(t=1)
Debug = None


class EntityRootError(Exception):
  """Root error class"""


class OverworldEntity(object):
  """docstring for OverworldEntity
  Hurt box refers to the entities whole hitbox relating to other entities
  Collision box refers to the entities feet relating to movement
  """
  TileLowerCollisionBox = AxisDistance(px=2)
  def __str__(self):
    return None

  def __init__(self, coord, config): #facing='N', moveSpeed=(0,4,0), customHitbox=None):
    """Class constructor
    Facing defaults to North
    Movespeed is measured in tiles per second originally, and is converted into pixels per frame
    """
    assert isinstance(coord, Coordinate), 'incorrect type of arg coord: should be type Coordinate, is type {}'.format(type(coord))
    self.hasMoved = False
    self.position = coord
    self.animationState = {'state': 0, 'frame': 0} #handled by gui
    
    self.name = config['name']
    self.facing = Direction(config['facing'])
    self.facingLinear = Direction(config['facing'])
    self.moveSpeed = AxisDistance(**config['moveSpeed'])
    self.__collisionBox = config.get('collisionBox', None)
    super(OverworldEntity, self).__init__()

  def collisionBox(self, coord=None):
    """Returns the collision box of the enemy"""
    coord = coord or self.position
    if self.__collisionBox is None:
      width = TilePixels
      height = OverworldEntity.TileLowerCollisionBox
    return BasicRectangleArea(coord, width, height)

  def hurtBox(self):
    """Returns the hurt box of the entity"""
    return BasicRectangleArea(self.position, TilePixels)

  def face(self, n):
    """Faces the character in a direction"""
    self.facing = Direction(n)
    if Direction.linear(n):
      self.facingLinear = Direction(n)

  def _move(self):
    """Unconditional move"""
    self.position = self.moveResultPos()

  def move(self, board, entities, face=None):
    """Conditional move
    Should only happen once per frame
    """
    self.face(face or self.facing)

    if Debug and self.hasMoved:
      pass #LOG FRAME ERROR

    if self.canMoveTo(self.moveResultPos(), board, entities):
      self._move()
      self.hasMoved = True

  def moveResultPos(self):
    return self.position.shiftDir(self.facing, self.moveSpeed)

  def canMoveTo(self, coord, board, entities):
    collisionBox = self.collisionBox(coord)
    entityCollision = bool(sum([ collisionBox in i.collisionBox() for i in entities if i is not self ]))

    tileCollision = False
    tiles = []
    for xinc in [(0, 0, 0), (1, 0, 0)]:
      for yinc in [(0, 0, 0), (1, 0, 0)]:
        nextCoord = (coord + Coordinate(xinc, yinc)).rounded(lvl='t')
        unpassable = not(board[nextCoord].passable())
        intersection = collisionBox in BasicRectangleArea(nextCoord, TilePixels)
        tileCollision |= unpassable & intersection
    return not(tileCollision or entityCollision)

  def tick(self):
    """Ticks the player and resets hasMoved
    Used to test the players movement for the gui
    """
    self.animationState['frame'] += 1
    self.hasMoved = False

  def isColliding(self, x):
    """Relates to movement"""
    assert isinstance(x, OverworldEntity) or isinstance(x, BasicRectangleArea), 'incorrect type of arg x: should be type BasicRectangleArea or OverworldEntity, is type {}'.format(type(x))
    if isinstance(x, OverworldEntity): x = x.collisionBox()
    return collisionBox.intersection(x)

  def isHit(self, x):
    """Returns whether the entity is colliding with another entity"""
    assert isinstance(x, OverworldEntity), 'incorrect type of arg x: should be type OverworldEntity, is type {}'.format(type(x))
    return self.hurtBox().intersection(x.hurtBox())
