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


UserInput = GuiModule.UserInput
ImageName = GuiModule.ImageName
DormantImage = GuiModule.DormantImage
ComplexImage = GuiModule.ComplexImage


class GuiEntityOverworld(ComplexImage):
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
            x, y = entity.pos.toPixels()
            image = self.entityName(entity)
            self.images[i].update(image, sx=x, sy=y)
        self.show()

    def layersort(self, a, b):
        """Sorts images by ycoord"""
        x = cmp(b.y, a.y)
        y = cmp(b.x, a.x)
        return x or y

    @staticmethod
    def entityName(e):
        """Returns the entitys image name"""
        face = str(e.facingLinear)
        state = e.animState()
        prefix = GuiEntityOverworld.imagePrefix
        return '-'.join([prefix, e.id, face, state])

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
        self.entities = GuiEntityOverworld(layer=2)
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
        super(Gui, self).__init__()
        self.images = {
            'board': Board(),
        }
        global sprites
        sprites = GuiModule.sprites
