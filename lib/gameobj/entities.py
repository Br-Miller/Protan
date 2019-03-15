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

from mixins import ig
from mixins.CoordPos import AxisDistance, BasicRectangleArea, Coordinate, Direction

TicksPerSecond = 60
TilePixels = AxisDistance(t=1)
Debug = None


class EntityRootError(Exception):
  """Root error class"""


class OverworldEntity(object):
  """Base overworld entity class
  Hurt box refers to the entities whole hitbox relating to other entities
  Collision box refers to the entities feet relating to movement
  """
  frameTime = 5
  TileLowerCollisionBox = AxisDistance(px=2)
  def __init__(self, coord, config):
    """Class constructor
    Facing defaults to North
    Movespeed is measured in tiles per second originally, and is converted into pixels per frame
    """
    assert isinstance(coord, Coordinate), 'incorrect type of arg coord: should be type Coordinate, is type {}'.format(type(coord))
    self.anims = self.animsCreate()
    self.prestate = False #moved last turn?
    self.hasmoved = False

    self.pos = coord
    self.name = config['name']
    self.facing = Direction(config['facing'])
    self.moveSpeed = AxisDistance(**config['moveSpeed'])
    self.facingLinear = Direction(config['facing'])
    super(OverworldEntity, self).__init__()

  def animsCreate(self):
    i = ig.Animation(OverworldEntity.frameTime, ['n', 'b'])
    w = ig.Animation(OverworldEntity.frameTime, ['l', 'r'])
    return { 'idle': i, 'walk': w }

  def animState(self):
    d = {True: 'walk', False: 'idle'}
    anim = self.anims[ d[self.hasmoved] ]

    if self.prestate != self.hasmoved:
      anim.rewind()
    anim.update()
    return anim.tile

  def collisionBox(self, coord=None):
    """Returns the collision box of the enemy"""
    coord = coord or self.pos
    width = TilePixels
    height = OverworldEntity.TileLowerCollisionBox
    return BasicRectangleArea(coord, width, height)

  def hurtBox(self):
    """Returns the hurt box of the entity"""
    return BasicRectangleArea(self.pos, TilePixels)

  def face(self, n):
    """Faces the character in a direction"""
    self.facing = Direction(n)
    if Direction.linear(n):
      self.facingLinear = Direction(n)

  def _move(self):
    """Unconditional move"""
    self.pos = self.moveResultPos()

  def move(self, board, entities, face=None):
    """Conditional move
    Should only happen once per frame
    """
    self.face(face or self.facing)

    if Debug and self.hasmoved:
      pass #LOG FRAME ERROR

    if self.canMoveTo(self.moveResultPos(), board, entities):
      self._move()
      self.hasmoved = True

  def moveResultPos(self):
    return self.pos.shiftDir(self.facing, self.moveSpeed)

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
    """Ticks the player and resets hasmoved
    Used to test the players movement for the gui
    """
    self.prestate = self.hasmoved
    self.hasmoved = False

  def isColliding(self, x): #UPDATE TO MAKE COLLISION
    """Relates to movement"""
    assert isinstance(x, OverworldEntity) or isinstance(x, BasicRectangleArea), 'incorrect type of arg x: should be type BasicRectangleArea or OverworldEntity, is type {}'.format(type(x))
    if isinstance(x, OverworldEntity): x = x.collisionBox()
    return collisionBox.intersection(x)

  def isHit(self, x):
    """Returns whether the entity is colliding with another entity"""
    assert isinstance(x, OverworldEntity), 'incorrect type of arg x: should be type OverworldEntity, is type {}'.format(type(x))
    return self.hurtBox().intersection(x.hurtBox())


class CombatEntity(object):
  """Base turn based entity combat class"""
  _lastId = 0
  damageCalculator = lambda atk, dfs: max([0, atk - dfs])
  def __init__(self, hp, atk, dfs, spd, man, ccr, exp, spatk):
    super(CombatEntity, self).__init__()
    self.health = hp
    self.attack = atk #Attack (Normal)
    self.armour = dfs #Defense
    self.speed = spd #Speed
    self.mana = man #Mana
    self.ccr = ccr #Critical Hit Ratio
    self.exp = exp #Experience
    self.spAttack = spatk #Special attack power

    self.anims = 0
    self.animSheet = 0
    self.currentAnim = 0

    self.identifier = CombatEntity._lastId
    self.pos = None #FIX UP
   #self.mag = mag #ADD OR NOT?
    CombatEntity._lastId += 1

  def destroy(self):
    pass #DESTROY ig.game.destroy(self)

  def attackNormal(self, e):
    e.recieveDamage(n)

  def attackSpecial(self):
    pass #Start minigame

  def dead(self):
    return self.hp <= 0

  def recieveDamage(self, n):
    self.hp -= CombatEntity.damageCalculator(n, self.dfs)

  def kill(self):
    self.hp = 0
