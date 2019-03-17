"""Game Entity code

All time is measured in ticks (60TicksPerSecond)
All distance is measured in AxisDistance

To do list
  Add customHitbox on EntityOverworld
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

class EntityOverworld(object):
  """Generic entity overworld class
  Hurt box refers to the entities whole hitbox relating to other entities
  Collision box refers to the entities feet relating to movement
  """
  frameTime = 15
  TileLowerCollisionBox = AxisDistance(px=2)
  configDefault = {
    'id': 'missingEntity',
    'name': 'MissingText',
    'move': {'p': 2},
    'face': 's',
  }
  def __init__(self, coord, config):
    """Class constructor
    Facing defaults to north
    Movespeed is measured in tiles per second and is converted into pixels per frame
    """
    assert isinstance(coord, Coordinate), 'incorrect type of arg coord: should be type Coordinate, is type {}'.format(type(coord))
    assert isinstance(config, dict), 'incorrect type of arg config: should be type dict, is type {}'.format(type(config))
    
    d = EntityOverworld.configDefault.copy()
    d.update(config)
    
    self.anims = self.animsCreate()
    self.prestate = False #Moved last turn
    self.hasmoved = False #Moved this turn

    self.pos = coord
    self.id = d['id']
    self.name = d['name']
    self.moveSpeed = AxisDistance(**d['move'])
    self.facing = Direction(d['face'])
    self.facingLinear = Direction(d['face'])
    super(EntityOverworld, self).__init__()

  def animsCreate(self):
    i = ig.Animation(EntityOverworld.frameTime, ['n', 'b'])
    w = ig.Animation(EntityOverworld.frameTime, ['l', 'r'])
    return { 'idle': i, 'walk': w }

  def animState(self):
    """Returns the current animation state"""
    d = {True: 'walk', False: 'idle'}
    anim = self.anims[ d[self.hasmoved] ]
    if self.prestate != self.hasmoved: anim.rewind()
    anim.update()
    return anim.tile

  def collisionBox(self, coord=None):
    """Returns the collision box of the enemy
    The collision box is the entities feet
    """
    coord = coord or self.pos
    width = TilePixels
    height = EntityOverworld.TileLowerCollisionBox
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
    """Conditional move"""
    self.face(face or self.facing)

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
    """Resets data from last frame
    Resets hasmoved and sets prestate
    Assists the gui
    """
    self.prestate = self.hasmoved
    self.hasmoved = False

  def isColliding(self, x): #UPDATE TO MAKE COLLISION
    """Relates to movement"""
    assert isinstance(x, EntityOverworld) or isinstance(x, BasicRectangleArea), 'incorrect type of arg x: should be type BasicRectangleArea or OverworldEntity, is type {}'.format(type(x))
    if isinstance(x, EntityOverworld): x = x.collisionBox()
    return collisionBox.intersection(x)

  def isHit(self, x):
    """Returns whether the entity is colliding with another entity"""
    assert isinstance(x, EntityOverworld), 'incorrect type of arg x: should be type OverworldEntity, is type {}'.format(type(x))
    return self.hurtBox().intersection(x.hurtBox())

class EntityCombat(object):
  """Generic turn based entity combat class"""
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

    self.identifier = EntityCombat._lastId
    self.pos = None #FIX UP
   #self.mag = mag #ADD OR NOT?
    EntityCombat._lastId += 1

  def destroy(self):
    pass #DESTROY ig.game.destroy(self)

  def attackNormal(self, e):
    e.recieveDamage(n)

  def attackSpecial(self):
    pass #Start minigame

  def dead(self):
    return self.hp <= 0

  def recieveDamage(self, n):
    self.hp -= EntityCombat.damageCalculator(n, self.dfs)

  def kill(self):
    self.hp = 0
