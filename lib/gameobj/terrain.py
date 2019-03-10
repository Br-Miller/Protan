"""
Terrain class
"""


#import statements


class Terrain(object):
	"""Base terrain class"""
	size = (1, 0, 0)
	defaultSettings = {
		'id': 0,
		'solid': True,
		'name': 'unknown',
		'image': 'missingTexture',
		'variations': {
			'none': 'missingTexture',
		},
	}
	def __init__(self, trueName, config):
		self._id = config['id']
		self.name = config['name']
		self._image = config['image']
		self._solid = config['solid']
		self.trueName = trueName
		super(Terrain, self).__init__()

	def __str__(self):
		return self.trueName

	def image(self):
		return self._image

	def passable(self):
		return not(self._solid)

	@property
	def solid(self):
		return self._solid

	@solid.setter
	def solid(self, x):
		raise Exception('Why is this being set?')
	


def getTerrain(s):
	"""Gets a terrain object"""
	return Terrain(s, TerrainList[str(s)])


TerrainList = {
	'.debug2': {'id': -2, 'name': 'DebugTerrain2', 'solid': True , 'image': 'terrain-debug2'},
	'.debug1': {'id': -1, 'name': 'DebugTerrain1', 'solid': False, 'image': 'terrain-debug1'},
}