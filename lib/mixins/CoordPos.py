"""
Mixins related to coordinates and positions handling and reading
STANDARD UNITS
1 Tile (t) <-> 32 Pixels
1 Pixel (px) <-> 8 Subpixels (sx)
"""


from warnings import warn


class AxisDistance(object):
    """Outputs distance and saves space
    Immutable
    """
    tilesize = 32
    pixelsize = 8
    def __init__(self, t=0, px=0, sx=0):
        """Class constructer
        Args:
            t: Tile
            px: Pixel
            sx: Subpixel
        """
        assert isinstance(t, int), 'incorrect type of arg t: should be type int, is type {}'.format(type(t))
        assert isinstance(px, int), 'incorrect type of arg px: should be type int, is type {}'.format(type(px))
        assert isinstance(sx, int), 'incorrect type of arg sx: should be type int, is type {}'.format(type(sx))
        self.tile = t
        self.pixel = px
        self.subpixel = sx
        self.cleanup()
        super(AxisDistance, self).__init__()

    def __iter__(self): #TO TUPLE
        return iter((self.tile, self.pixel, self.subpixel))

    def __str__(self): #TO STRING
        return '{}.{}.{}'.format(self.tile, self.pixel, self.subpixel)

    def __repr__(self): #TO Human STRING
        return '{}t{}px{}sx'.format(self.tile, self.pixel, self.subpixel)

    @classmethod
    def fromStr(cls, s):
        assert isinstance(s, str), 'incorrect type of arg s: should be type str, is type {}'.format(type(s))
        s = [ int(n) for n in s.split('.') ]
        return cls(*s)

    def __add__(self, x):
        assert isinstance(x, AxisDistance), 'incorrect type of arg x: should be type AxisDistance, is type {}'.format(type(x))
        tile = self.tile + x.tile
        pixel = self.pixel + x.pixel
        subpixel = self.subpixel + x.subpixel
        return AxisDistance(t=tile, px=pixel, sx=subpixel)

    def __hash__(self):
        return hash(tuple(self))

    def __neg__(self):
        tile = -self.tile
        pixel = -self.pixel
        subpixel = -self.subpixel
        return AxisDistance(t=tile, px=pixel, sx=subpixel)

    def __rmul__(self, x):
        assert isinstance(x, int), 'incorrect type of arg x: should be type int, is type {}'.format(type(x))
        return self.__mul__(x)

    def __mul__(self, x):
        assert isinstance(x, int) or isinstance(x, float), 'incorrect type of arg x: should be type int or float, is type {}'.format(type(x))
        tile = int(self.tile * x)
        pixel = int(self.pixel * x)
        subpixel = int(self.subpixel * x)
        return AxisDistance(t=tile, px=pixel, sx=subpixel)

    def __sub__(self, x):
        assert isinstance(x, AxisDistance), 'incorrect type of arg x: should be type AxisDistance, is type {}'.format(type(x))
        tile = self.tile - x.tile
        pixel = self.pixel - x.pixel
        subpixel = self.subpixel - x.subpixel
        return self.AxisDistance(t=tile, px=pixel, sx=subpixel)

    def __cmp__(self, x):
        assert isinstance(x, AxisDistance), 'incorrect type of arg x: should be type AxisDistance, is type {}'.format(type(x))
        a = [
            cmp(self.tile, x.tile),
            cmp(self.pixel, x.pixel),
            cmp(self.subpixel, x.subpixel)
        ]
        for i in a:
            if i != 0:
                return i
        return 0

    def __eq__(self, x):
        assert isinstance(x, AxisDistance), 'incorrect type of arg x: should be type AxisDistance, is type {}'.format(type(x))
        return self.__cmp__(x) == 0

    def __ne__(self, x):
        assert isinstance(x, AxisDistance), 'incorrect type of arg x: should be type AxisDistance, is type {}'.format(type(x))
        return self.__cmp__(x) != 0

    def __ge__(self, x):
        assert isinstance(x, AxisDistance), 'incorrect type of arg x: should be type AxisDistance, is type {}'.format(type(x))
        y = self.__cmp__(x)
        return y == 0 or y == 1

    def __lt__(self, x):
        assert isinstance(x, AxisDistance), 'incorrect type of arg x: should be type AxisDistance, is type {}'.format(type(x))
        return self.__cmp__(x) == -1

    def __le__(self, x):
        assert isinstance(x, AxisDistance), 'incorrect type of arg x: should be type AxisDistance, is type {}'.format(type(x))
        y = self.__cmp__(x)
        return y == 0 or y == -1

    def __gt__(self, x):
        assert isinstance(x, AxisDistance), 'incorrect type of arg x: should be type AxisDistance, is type {}'.format(type(x))
        return self.__cmp__(x) == 1

    def _abs(self):
        if self.tile < 0:
            return -AxisDistance(t=self.tile, px=self.pixel, sx=self.subpixel)
        return AxisDistance(t=self.tile, px=self.pixel, sx=self.subpixel)

    def copy(self):
        return AxisDistance(t=self.tile, px=self.pixel, sx=self.subpixel)
    
    def cleanup(self):
        """Reduces the lower units"""
        self.subpixel, self.pixel = self.stepup(self.subpixel, self.pixel, AxisDistance.pixelsize)
        self.pixel, self.tile = self.stepup(self.pixel, self.tile, AxisDistance.tilesize)

    def stepup(self, lowUnit, highUnit, higherBound):
        """Steps the lower number to the higher number if it is lower than zero or higher than higherBound"""
        if lowUnit >= higherBound:
            highUnit += lowUnit / higherBound #PYTHON3 //
            lowUnit = lowUnit % higherBound

        elif lowUnit < 0:
            highUnit += (lowUnit / higherBound) - 1  #PYTHON3 //
            lowUnit += abs(lowUnit / higherBound * lowUnit) + higherBound

        return lowUnit, highUnit
    
    def rounded(self, lvl='p'):
        """Rounds down to the nearest pixel or tile"""
        d = {
            'p': {'t': self.tile, 'px': self.pixel},
            't': {'t': self.tile},
        }
        return AxisDistance(**d[lvl])
    
    def limit(self, _min, _max):
        if _min > self:
            return _min
            
        elif _max < self:
            return _max
        
        else:
            return self

    def toTiles(self):
        return self.tile

    def toPixels(self):
        """Converts the distance to the nearest pixel as an int"""
        return (self.tile * AxisDistance.tilesize) + self.pixel

    def toSubpixels(self):
        warn(Warning("Function {} is not reccommended for use".format(__func__.__name__)))
        return (((self.tile * AxisDistance.tilesize) + self.pixel) * AxisDistance.pixelsize) + self.subpixel

    def inRange(self, lower, higher):
        assert isinstance(lower, AxisDistance), 'incorrect type of arg lower: should be type AxisDistance, is type {}'.format(type(lower))
        assert isinstance(higher, AxisDistance), 'incorrect type of arg higher: should be type AxisDistance, is type {}'.format(type(higher))
        return lower <= self < higher


class Direction(object):
    """Contains basic directions and their displacement
    Inherits int
    """
    strtoint = {
        'n' : 0,
        'ne': 1,
        'e' : 2,
        'se': 3,
        's' : 4,
        'sw': 5,
        'w' : 6,
        'nw': 7,
        'c' : 8,
    }
    displacement = {
        0: [0, 1],
        1: [1, 1],
        2: [1, 0],
        3: [1, -1],
        4: [0, -1],
        5: [-1, -1],
        6: [-1, 0],
        7: [-1, 1],
        8: [0, 0],
    }
    directions = {
        0: 'n',
        1: 'ne',
        2: 'e',
        3: 'se',
        4: 's',
        5: 'sw',
        6: 'w',
        7: 'nw',
        8: 'c',
    }
    def __str__(self):
        return Direction.directions[self.direction]

    def __repr__(self):
        return Direction.directions[self.direction]

    def __init__(self, direction):
        assert isinstance(direction, int) or isinstance(direction, str) or isinstance(direction, Direction), 'incorrect type of arg direction: should be type int, Direction or str, is type {}'.format(type(direction))
        self._dx = None
        self._dy = None
        if isinstance(direction, str):
            direction = Direction.strtoint[direction] 
        elif isinstance(direction, Direction):
            direction = direction.direction
        self.direction = direction

    def isDiagonal(self):
        """Whether this direction is a diagonal one."""
        raise Exception('Deprecated')
        return self.direction % 2 == 1

    def opposite(self):
        """Returns the direction opposite this one, or Center if it's Center"""
        if self.direction == 8: return Direction(8)
        n = self.direction + 4
        if n >= 8: n -= 8
        return Direction(n)

    @staticmethod
    def oblique(n):
        return n in [1, 3, 5, 7] or n not in ['n', 's', 'e', 'w', 'c']

    @staticmethod
    def linear(n):
        return n in [0, 2, 4, 6] or n in ['n', 's', 'e', 'w']


    @staticmethod
    def isDir(n):
        """Returns whether int n or str n is considered a direction. Directions include numbers 0 to 8"""
        assert isinstance(n, int) or isinstance(n, str) or isinstance(n, Direction), 'incorrect type of arg n: should be type int, str or Direction, is type {}'.format(type(n))
        dd = n in Direction.directions
        ds = n in Direction.strtoint
        return dd or ds or isinstance(n, Direction)

    @property
    def dx(self):
        """Returns the x displacement of the direction"""
        return self._dx

    @dx.getter
    def dx(self):
        return Direction.displacement[self.direction][0]

    @property
    def dy(self):
        """Returns the y displacement of the direction"""
        return self._dy

    @dx.getter
    def dy(self):
        return Direction.displacement[self.direction][1]
    

class CoordList(list):
    """A custom list for containing Coordinate Class instances
    This class contains coordinates relative to a base coordinate
    Inherits list
    """
    def __init__(self, basecoord, *args):
        args = self.formatInput(args)
        self.basecoord = Coordinate(*basecoord)
        super(CoordList, self).__init__(*args)

    def __getitem__(self, n):
        coord = super(CoordList, self).__getitem__(n)
        coord = coord.shift(self.basecoord)
        return coord

    def __iter__(self):
        l = [ coord.shift(self.basecoord) for coord in super(CoordList, self).__iter__() ]
        return iter(l)

    def __add__(self, cl):
        x, y = CoordIt.formatCoord(self.basecoord, to=tuple)
        l = [ (c.x - x, c.y - y) for c in cl.exact() ]
        
    def exact(self):
        return [ c for c in self ]

    def flip(self, axis='x'):
        l = map(lambda x: x.flip(axis=axis), self)
        return CoordList(self.basecoord, l)

    def shift(self, x, y=None):
        x1, y1 = self.basecoord
        x2, y2 = CoordIt.formatCoord(self.basecoord, to=tuple)
        self.basecoord = (x2 - x1, y2 - y1)

    @staticmethod
    def formatInput(l):
        return [ CoordIt.formatCoord(c, to='coord') for c in l ]

    @property
    def basecoord(self):
        return self._basecoord

    @basecoord.setter
    def basecoord(self, x, y=None):
        coord = self.formatCoord(x, y=y, to='coord')
        self._basecoord = coord


class Coordinate(object):
    """Coordinate class to allow for easy access to coordinate functions
    There are three sizes. Tile > Pixel > Subpixel
    Another size, AREA may be implemented
    """
    def __init__(self, x, y=None):
        if isinstance(x, Coordinate) and y is None:
            x, y = x.x, x.y
        elif isinstance(x, tuple) and isinstance(y, tuple):
            x, y = AxisDistance(*x), AxisDistance(*y)
        self.x = x
        self.y = y

    @classmethod
    def fromStr(cls, s):
        """docstring for fromStr"""
        s = s[1:-1].split(', ')
        s = [ AxisDistance.fromStr(i) for i in s ]
        return cls(*s)

    def __str__(self):
        return '(%s, %s)' % (str(self.x), str(self.y))

    def __repr__(self):
        return '(%s, %s)' % (repr(self.x), repr(self.y))

    def __iter__(self):
        return iter((tuple(self.x), tuple(self.y)))

    def __hash__(self):
        return hash(tuple(self))

    def __add__(self, coord):
        """alias for the this classes function shift()"""
        assert isinstance(coord, Coordinate), "incorrect type of arg coord: should be Coordinate, is {}".format(type(coord))
        return self.shift(coord)

    def __eq__(self, x):
        if isinstance(x, Coordinate):
            return self.x == x.x and self.y == x.y
        return False

    def __getitem__(self, n):
        assert isinstance(n, int), 'incorrect type of arg n: should be type int, is type {}'.format(type(n))
        assert n == 0 or n == 1, "invalid value of arg n: should be 0 or 1, is {}".format(coord)
        return {0: self.x, 1: self.y}[n]

    def __sub__(self, coord):
        """similar to __add__(), but flips the coordinate in the both axis's first"""
        assert isinstance(coord, Coordinate), "incorrect type of arg coord: should be Coordinate, is {}".format(type(coord))
        coord = coord.flip('xy')
        return self.shift(coord)
    
    def copy(self):
        return Coordinate(self.x.copy(), self.y.copy())

    def shift(self, coord, y=None):
        """Returns a new Coordinate instance, shifted this by arg coord"""
        assert isinstance(coord, Coordinate) or isinstance(y, AxisDistance), "incorrect type of arg coord: should be Coordinate or AxisDistance, is {}".format(type(coord))
        if y is not None: coord = Coordinate(coord, y)
        x1, y1 = (self.x, self.y)
        x2, y2 = (coord.x, coord.y)
        x = x1 + x2
        y = y1 + y2
        return Coordinate(x, y)

    def shiftDir(self, direction, n):
        """Returns a new Coordinate instance, shifted in the given direction"""
        assert Direction.isDir(direction), "incorrect type of arg direction: should be a Direction, is {}".format(type(direction))
        assert isinstance(n, AxisDistance), 'incorrect type of arg n: should be type AxisDistance, is type {}'.format(type(n))
        x, y = self.x, self.y
        direction = Direction(direction)
        x += direction.dx * n
        y += direction.dy * n
        return Coordinate(x, y)

    def distTo(self, coord, total=True):
        """Returns this instances distance to the given coordinate.
        If total is False, returns a new Coordinate object
        """
        assert isinstance(coord, Coordinate), "incorrect type of arg coord: should be Coordinate, is {}".format(type(coord))
        assert isinstance(total, bool), "incorrect type of arg total: should be bool, is {}".format(type(total))

        x1, y1 = self.x, self.y
        x2, y2 = coord.x, coord.y
        d = {
            True: (x2 - x1)._abs() + (y2 - y1)._abs(),
            False: Coordinate(x2 - x1, y2 - y1),
        }
        return d[total]

    def trigDist(self, coord):
        """Returns the trigonometry distance to a point"""
        assert isinstance(coord, Coordinate), "incorrect type of arg coord: should be Coordinate, is {}".format(type(coord))

        x1, y1 = self.x, self.y
        x2, y2 = coord.x, coord.y
        xdis = abs(x1 - x2) ** 2
        ydis = abs(y1 - y2) ** 2
        dist = float(xdis + ydis) ** 0.5
        return dist

    def dirTo(self, coord):
        assert isinstance(coord, Coordinate), "incorrect type of arg coord: should be Coordinate, is {}".format(type(coord))

        dist = self.distTo(coord, total=False)
        dist = map(lambda n: cmp(n, 0), dist)
        dirDict = Direction.directions.items()

        for k, v in Direction.displacement.items():
            if v == rdis:
                return k

        raise ValueError('Unknown error has occured')

    def inBounds(self, coordMin, coordMax=None):
        """Returns whether self is in bounds"""
        if coordMax == None:
            coordMax = coordMin
            coordMin = Coordinate(AxisDistance(), AxisDistance())

        xMin = coordMin.x
        xMax = coordMax.x
        yMin = coordMin.y
        yMax = coordMax.y
        inX = self.x.inRange(xMin, xMax)
        inY = self.x.inRange(yMin, yMax)
        return inX & inY

    def rounded(self, lvl='p'):
        return Coordinate(self.x.rounded(lvl), self.y.rounded(lvl))

    def flip(self, axis='x'):
        d = {
            'x': (-self.x, self.y),
            'y': (self.x, -self.y),
            'xy': (-self.x, -self.y),
        }
        return Coordinate(*d[axis])
    
    def limit(self, _min, _max):
        x = self.x.limit(_min, _max)
        y = self.y.limit(_min, _max)
        return Coordinate(x, y)
        
    def toPixels(self):
        return (self.x.toPixels(), self.y.toPixels())
    

class BasicRectangleArea(object):
    """docstring for BasicRectangleArea"""
    def __contains__(self, rectangleArea):
        return self.intersection(rectangleArea)

    def __init__(self, basecoord, w, h=None):
        h = h or w
        self.xArea = (basecoord[0], basecoord[0] + w)
        self.yArea = (basecoord[1], basecoord[1] + h)

    @staticmethod
    def _intersection(x, y):
        """Determines whether there is an intersection in two ranges"""
        a, b = x
        c, d = y
        return (d > a) and (c < b)

    def intersection(self, x):
        """Returns whether this rectangle will intersect"""
        _x = self._intersection(self.xArea, x.xArea)
        _y = self._intersection(self.yArea, x.yArea)
        return _x and _y
        
        
