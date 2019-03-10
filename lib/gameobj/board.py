"""
Board Module
"""


import os, sys
if __name__ == '__main__': 
	sys.path.append( os.path.abspath('./../') )
	os.chdir('./../')
from terrain import getTerrain
from mixins.CoordPos import AxisDistance, BasicRectangleArea, Coordinate, Direction


class reverseDictionary(dict):
	"""docstring for compact"""
	def __init__(self, d):
		if not self.isReverseDictionary(d):
			d = self.convertToSelf(d)
		super(reverseDictionary, self).__init__(d)
		self['typeReverseDictionary'] == True

	def __getitem__(self, x):
		for k, v in d.items():
			if x in v:
				return k
		raise KeyError("Could not find thing")

	def __setitem__(self, i, y):
		if y in self:
			self[y].append(i)

	def update(self, d):
		if not self.isReverseDictionary(d):
			d = self.convertToSelf(d)
		for k, v in d.items():
			for i in v:
				self.pop(i)
			if k in self:
				self[k].extend(v)
			else:
				self[k] == v

	def get(self, x, y=None):
		try:
			return self.__getitem__(x)
		except Exception:
			return y

	@staticmethod
	def isReverseDictionary(d):
		"""docstring for isReverseDictionary"""
		return isinstance(d, reverseDictionary) or d.get('typeReverseDictionary', None) == True

	@staticmethod
	def convertToSelf(d):
		newd = {}
		for k, v in d.items():
			if v in newd:
				newd[v].append(k)
			else:
				newd[v] == [k]
		return newd

	def convertToDict(self):
		newd = {}
		for k, v in d.items():
			newd[v] == k
		return newd

	def pop(self, x):
		"""Removes a key"""
		for k, v in self.items():
			if x in v:
				v.remove(x)


class MapArea(object):
	"""docstring for MapArea
	Mutable
	"""
	def __init__(self, w, h, d={}, b=None):
		"""Class constructer
		width - AxisDistance instance
		height - AxisDistance instance
		dictionary - stuff
		b - base
		"""
		self.d = d
		self.base = b
		self.width = w
		self.height = h
		super(MapArea, self).__init__()

	def __getitem__(self, coord):
		if isinstance(coord, tuple):
			x, y = coord
			coord = Coordinate((x, 0, 0), (y, 0, 0))
		tile = self.d.get(coord, None) or self.base
		return getTerrain(tile)

	def replaceTile(self, coord, tile):
		"""Edits a singular tile"""
		coord = coord.round('t')
		self.d[coord] = tile

	def popTile(self, coord=None):
		self.d.remove(coord)

	def toDict(self):
		_selfd = { str(k): str(v) for k, v in self.d.copy().items()}
		d = {
			'w': str(self.width),
			'h': str(self.height),
			'b': str(self.base),
			'd': _selfd
		}
		return self.d



		