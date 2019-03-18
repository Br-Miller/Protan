"""Bullet hell type minigame
The bullet hell minigame system
"""


import Math
from mixins.CoordIt import Coordinate


class Counter(object):
    def __init__(self, n=0)
        self.cache = n
        
    def __call__(self):
        n = self.cache
        self.cache += 1
        return n

class ImpactMap(object):
    def init(tilesize, data):
        self.name = None
        self.tilesize = tilesize #int
        self.data = data #matrix
        self.height = len(data)
        self.width = len(data[0])

    def getTile(x, y):
        tx = int(x / self.tilesize)
        ty = int(y / self.tilesize)
        if (tx >= 0 and tx < self.width) and (ty >= 0 and ty < self.height):
            return self.data[ty][tx]
        else:
            return 0
        
    def setTile(x, y, tile):
        tx = int(x / self.tilesize)
        ty = int(y / self.tilesize)
        if (tx >= 0 and tx < self.width) and (ty >= 0 and ty < self.height):
            self.data[ty][tx] = tile

    
class EntityBH(object):
    id = Counter()
    COLLIDES = {
        'NEVER': 0,
        'LIGHT': 1,
        'PASSIVE': 2,
        'ACTIVE': 4,
        'FIXED': 8
    }
    TEAMTYPE = {
        'NONE': 0,
        'A': 1,
        'B': 2,
        'BOTH': 3
    }
    defaultconfig = {
        'sx': 16,
        'sy': 16,
        'vx': 0,
        'vy': 0,
        'ax': 0,
        'ay': 0,
        'mv': 100
    }
    def __init__(self, x, y, config):
        self.id = EntityBH.id()
        self.pos = Coordinate(x, y)
        self.size = Coordinate(config['sx'], config['sy'])
        self.last = Coordinate(x, y)
        self.vel = Coordinate(config['vx'], config['vy'])
        self.accel = Coordinate(config['ax'], config['ay'])
        self.maxvel = (-AxisDistance(**config['mv']), AxisDistance(**config['mv']))
        self.type = None
        self.checkAgainst = None
        self.collides = None
        self.killed = False
        
    def animState(self):
        return None
        
    def addAnim(self):
        raise NotImplementedError('Not implemented yet')
        
    def update(self):
        self.last = self.pos
        self.vel = self.getNewVelocity
        
    def getNewVelocity(self, v, a, m):
        v += a
        return v.limit(*maxvel)
        
    def touches(x):
        return not(self.pos.x >= x.pos.x + x.size.x or self.pos.x + self.size.x <= x.pos.x or self.pos.y >= x.pos.y + x.size.y or self.pos.y + self.size.y <= x.pos.y)
        
    def distanceTo(x):
        xd = (self.pos.x + self.size.x / 2) - (x.pos.x + x.size.x / 2)
        yd = (self.pos.y + self.size.y / 2) - (x.pos.y + x.size.y / 2)
        return Math.sqrt(xd**2 + yd**2)
        
    def angleTo(x):
        return Math.atan2((x.pos.y + x.size.y / 2) - (self.pos.y + self.size.y / 2), (x.pos.x + x.size.x / 2) - (self.pos.x + self.size.x / 2))
        
    def check(x):
        pass
        
    def collideWith(x, axis):
        pass
    
    def ready():
        pass
        
    @staticmethod
    def checkPair(a, b):
        if a.checkAgainst and b.type:
            a.check(b)

        if b.checkAgainst and a.type:
            b.check(a)

        if a.collides and b.collides and a.collides + b.collides > EntityBH.COLLIDES['ACTIVE']:
            EntityBH.solveCollision(a, b)
            
    @staticmehtod
    def solveCollision(a, b):
        weak = None
        if (a.collides == EntityBH.COLLIDES['LITE'] or b.collides == EntityBH.COLLIDES['FIXED']:
            weak = a

        elif (b.collides == EntityBH.COLLIDES['LITE'] or a.collides == EntityBH.COLLIDES['FIXED']:
            weak = b

        if (a.last.x + a.size.x > b.last.x and a.last.x < b.last.x + b.size.x):
            if (a.last.y < b.last.y):
                EntityBH.seperateOnYAxis(a, b, weak)

            else:
                EntityBH.seperateOnYAxis(b, a, weak)

            a.collideWith(b, 'y')
            b.collideWith(a, 'y')

        elif (a.last.y + a.size.y > b.last.y and a.last.y < b.last.y + b.size.y):
            if (a.last.x < b.last.x) {
                EntityBH.seperateOnXAxis(a, b, weak)
            else:
                EntityBH.seperateOnXAxis(b, a, weak)
            a.collideWith(b, 'x')
            b.collideWith(a, 'x')

    def seperateOnXAxis(left, right, weak):
        nudge = (left.pos.x + left.size.x - right.pos.x)
        if weak
            strong = right if left is weak else left
            weak.vel.x = -weak.vel.x * weak.bounciness + strong.vel.x
            resWeak = ig.game.collisionMap.trace(weak.pos.x, weak.pos.y, weak == left ? -nudge : nudge, 0, weak.size.x, weak.size.y)
            weak.pos.x = resWeak.pos.x
        else:
            v2 = (left.vel.x - right.vel.x) / 2
            left.vel.x = -v2
            right.vel.x = v2
            resLeft = ig.game.collisionMap.trace(left.pos.x, left.pos.y, -nudge / 2, 0, left.size.x, left.size.y)
            left.pos.x = Math.floor(resLeft.pos.x)
            resRight = ig.game.collisionMap.trace(right.pos.x, right.pos.y, nudge / 2, 0, right.size.x, right.size.y)
            right.pos.x = Math.ceil(resRight.pos.x)

    def seperateOnYAxis(top, bottom, weak):
        nudge = (top.pos.y + top.size.y - bottom.pos.y)
        if weak:
            strong = top === weak ? bottom : top
            weak.vel.y = -weak.vel.y * weak.bounciness + strong.vel.y
            nudgeX = 0
            if (weak == top and Math.abs(weak.vel.y - strong.vel.y) < weak.minBounceVelocity):
                weak.standing = true
                nudgeX = strong.vel.x * ig.system.tick
                
            resWeak = ig.game.collisionMap.trace(weak.pos.x, weak.pos.y, nudgeX, weak == top ? -nudge : nudge, weak.size.x, weak.size.y)
            weak.pos.y = resWeak.pos.y
            weak.pos.x = resWeak.pos.x
            
        elif (ig.game.gravity and (bottom.standing or top.vel.y > 0)):
            resTop = ig.game.collisionMap.trace(top.pos.x, top.pos.y, 0, -(top.pos.y + top.size.y - bottom.pos.y), top.size.x, top.size.y)
            top.pos.y = resTop.pos.y
            if (top.bounciness > 0 and top.vel.y > top.minBounceVelocity):
                top.vel.y *= -top.bounciness

            else:
                top.standing = true
                top.vel.y = 0

        else:
            v2 = (top.vel.y - bottom.vel.y) / 2
            top.vel.y = -v2
            bottom.vel.y = v2
            nudgeX = bottom.vel.x * ig.system.tick
            resTop = ig.game.collisionMap.trace(top.pos.x, top.pos.y, nudgeX, -nudge / 2, top.size.x, top.size.y)
            top.pos.y = resTop.pos.y
            resBottom = ig.game.collisionMap.trace(bottom.pos.x, bottom.pos.y, 0, nudge / 2, bottom.size.x, bottom.size.y)
            bottom.pos.y = resBottom.pos.y
            

    
        
