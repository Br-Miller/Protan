"""Main graphical module
Uses guipygame or guitkinter to render images
"""


import os
import sys

if __name__ == '__main__':
    sys.path.append(os.path.abspath('../'))
    os.chdir('../')

try:
    import gui.guipygame as GuiModule

except ImportError:
    import gui.guitkinter as GuiModule        


sprites = GuiModule.sprites
ImageName = GuiModule.ImageName
imageDict = GuiModule.imageDict #Should not be needed
DormantImage = GuiModule.DormantImage
ComplexImage = GuiModule.ComplexImage


class GuiOverworldEntities(ComplexImage):
    """Overworld entity class"""
    imagePrefix = 'entity'
    def __init__(self, layer=1):
        self.x = 0
        self.y = 0
        self.layer = layer
        self.images = []

    def cleanup(self, l):
        excessImages = len(self.images) - len(l)
        for _ in range(excessImages):
            self.images.pop(0)

        for _ in range(-excessImages):
            self.images.append(DormantImage(0, 0, 'blank'))

    def update(self, l):
        self.hide()
        self.cleanup(l)

        for i, entity in enumerate(l):
            x, y = entity.position.toPixels()
            image = self.entityName(entity)
            self.images[i].update(image, sx=x, sy=y)
        self.show()

    def layersort(self, x, y):
        """Sorts images by ycoord"""
        a = cmp(y.y, x.y)
        if a == 0: 
            return cmp(y.x, x.x)
        return a

    @staticmethod
    def entityName(e):
        """Returns the entitys image name"""
        face = str(e.facingLinear)
        state = e.animState()
        prefix = GuiOverworldEntities.imagePrefix
        return '-'.join([prefix, e.name, face, state])

    @staticmethod
    def entityLegdir(e):
        """docstring for entityLegdir"""
        if e.animationState['frame'] >= GuiOverworldEntities.animationSpeed:
            e.animationState['frame'] = 0
            e.animationState['state'] = not(e.animationState['state']) #To 1 or 0. Toggles
        legdir = GuiOverworldEntities.animations
        return legdir[e.hasMoved][e.animationState['state']]

class GuiOverworldTerrain(ComplexImage):
    """docstring for Terrain"""
    def __init__(self, layer=1):
        self.x = 0
        self.y = 0
        self.layer = layer
        self.images = []
        self.terrain = []
        for x in range(GuiModule.BoardWidth):
            a = []
            for y in range(GuiModule.BoardHeight):
                img = DormantImage(x*32, y*32, 'terrain-debug1', layer=4)
                a.append(img)
            self.images.extend(a)
            self.terrain.append(a)
        super(GuiOverworldTerrain, self).__init__()

    def update(self, board):
        for x in range(GuiModule.BoardWidth):
            for y in range(GuiModule.BoardHeight):
                image = board[x, y].image()
                image = ImageName(image)
                self.terrain[x][y].update(image)

class Board(ComplexImage):
    """Board for gui"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.layer = 4
        self.terrain = GuiOverworldTerrain(layer=4)
        self.entities = GuiOverworldEntities(layer=2)
        self.images = [self.terrain, self.entities]
        super(Board, self).__init__()
        
    def update(self, board, entities):
        self.terrain.update(board)
        self.entities.update(entities)

    def show(self):
        self.terrain.show()


class Gui(GuiModule.GuiBase):
    """Main gui module for the game"""
    def __init__(self):
        """Class constructor"""
        self.images = {
            'board': Board(),
        }
