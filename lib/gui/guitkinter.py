"""Placeholder graphics
Placeholder for graphics
"""


import os
import re
import sys
import time
import warnings


if __name__ == '__main__':
    sys.path.append(os.path.abspath('../'))
    os.chdir('../')

try:
    from tkinter import Canvas, Tk, PhotoImage
except ImportError:
    from Tkinter import Canvas, Tk, PhotoImage

from dat.reqImages import ReqImages #GET REQUIRED IMAGES
from mixins.fileHandling import freader

tk_border = 6    #Compensates for tkinters 6 pixel border
base_size = [960, 640, 32]
maxSprites = 3000
BoardWidth = 30
BoardHeight = 20


class GuiError(Exception):
    """Class Error"""

class ActiveError(GuiError):
    """Something active and attempted to be reactivated"""
        
#--------------------------------------------------------------------

class ImageName(object):
    """Generalises image names"""
    optionHeader = '  -'
    imageNameRegex = re.compile('^[^ ]*')
    optionSuffixRegex = re.compile('{}[sxy][^ ]*'.format(optionHeader))
    options = {
        's': 'shade',
        'x': 'xsize',
        'y': 'ysize',
        'r': 'rspin'
    }
    def __init__(self, s=None, name=None, shade=0, xsize=1, ysize=1, rspin=0):
        if isinstance(s, str):
            name, shade, xsize, ysize, rspin = self.expandString(s)

        elif isinstance(s, ImageName):
            name, shade, xsize, ysize = s.name, s.shade, s.xsize, s.ysize, s.rspin

        self.name = name
        self.shade = shade
        self.xsize = xsize
        self.ysize = ysize
        self.rspin = sprites.getResolution(name, xsize, ysize, rspin)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        name = self.name
        shade = self.optionHeader + 's' + str(self.shade)
        xsize = self.optionHeader + 'x' + str(self.xsize)
        ysize = self.optionHeader + 'y' + str(self.ysize)
        rspin = self.optionHeader + 'r' + str(self.rspin) 
        return '{} {}{}{}'.format(name, shade, xsize, ysize, rspin) 

    def base(self):
        """Returns the base name of this image"""
        return ImageName(name=self.name)

    @classmethod
    def str(cls, s):
        """docstring for str"""
        assert isinstance(s, str), 'incorrect type of arg s: should be type str, is type {}'.format(type(s))
        return str(cls(s))

    @staticmethod
    def getArgs(s):
        """Gets arguments"""
        argType = s[3]
        argInfo = s[4:]
        argConv = lambda x: int(x)
        k = ImageName.options[argType]
        v = argConv(argInfo)
        return {k: v}

    @staticmethod
    def expandString(s):
        """Expands string information"""
        d = {
            'name': None,
            'shade': 0,
            'xsize': 1,
            'ysize': 1,
            'rspin': 0
        }
        d.update({'name': re.search(ImageName.imageNameRegex, s).group()})
        options = re.findall(ImageName.optionSuffixRegex, s)
        for s in options: d.update(ImageName.getArgs(s))
        return d['name'], d['shade'], d['xsize'], d['ysize'], d['rspin']

#--------------------------------------------------------------------

class SpriteEditor():
    """Sprite editing functions"""
    resolutions = [1, 2, 3, 5, 6, 9, 10, 15, 30, 45, 90]
    imageResCache = {}
    @staticmethod
    def _imageRes(imageLen, pixels=2):
        """calculates the maximum noticable shift"""
        d = SpriteEditor.imageResCache
        if imageLen in d.keys():
            return d[imageLen]
        
        rad = math.atan(float(pixels) / imageLen)
        deg = math.toDeg(rad)
        res = max([ i for i in SpriteEditor.resolutions if i < deg ])
        d.update({imageLen: res})
        return res
    
    @staticmethod
    def imageRes(image, deg, pixels=2):
        l = max([image.width(), image.height()])
        res = SpriteEditor._imageRes(l, pixels)
        dif = deg % res
        deg -= dif
        if diff > res / 2.0:
            deg += res
        return int(deg)
         
    @staticmethod
    def rotateimg(image, degrees):
        degrees = SpriteEditor._posdegree(degrees)
        d = {
            0: lamda x, d: x,
            90: SpriteEditor._turnImage,
            180: 'FUNCTION',
            270: SpriteEditor._turnImage
        }
        func = d.get(degrees, SpriteEditor._rotateImage)
        return func(image, degrees)
    
    @staticmethod
    def _posdegree(degrees):
        while degrees < 0:
            degrees += 360
        return degrees
    
    @staticmethod
    def _flipImage(image, degrees, axis='y'):
        assert degrees == 180, 'degrees should be 180: is {}'.format(degrees)
        func = {
            'x': lambda x, y: image.width() - x, y,
            'y': lambda x, y: x, image.height() - y
        }
        func = func[axis]
        w = image.width()
        h = image.height()
        newimage = PhotoImage(width=w, height=h)
        for x in range(w):
            for y in range(h):
                dx, dy = func(x, y)
                rgb = SpriteEditor.getpixel(image, x, y)
                SpriteEditor.setpixel(newimage, dx, dy, *rgb)
            
    @staticmethod
    def _turnImage(image, degrees):
        assert degrees == 90 or degrees == 270, 'degrees should be 90 or 270: is {}'.format(degrees)
        w = image.width()
        h = image.height()
        func = {
            90: lambda x, y: h - y, x,
            270: lambda x, y: y, w - x
        }
        func = func[degrees]
        newimage = PhotoImage(width=h, height=w)
        
        for x in range(w):
            for y in range(h):
                dx, dy = func(x, y)
                rgb = SpriteEditor.getpixel(image, x, y)
                SpriteEditor.setpixel(newimage, dx, dy, *rgb)
        return newimage
        
    @staticmethod
    def _rotateImage(image, degrees):
        radians = degrees * math.pi / 180
        tangent = -math.tan(radians/2)
        sine = math.sin(radians)
        image = SpriteEditor.shearImage(image, tangent, 'x')
        image = SpriteEditor.shearImage(image, sine, 'y')
        image = SpriteEditor.shearImage(image, tangent, 'x')
        return image
        
    @staticmethod
    def shearImage(image, gamma, axis):
        d = {
            'x': SpriteEditor.shearImageX,
            'y': SpriteEditor.shearImageY
        }
        func = d[axis]
        return func(image, gamma)

    @staticmethod
    def shearImageX(image, gamma):
        yresize = image.height()
        xresize = int(image.width() * (abs(gamma) + 1))
        newimag = PhotoImage(width=xresize, height=yresize)
        shftdir = {True: 0, False: image.height()}[(gamma < 0)]
        lnshift = lambda z: abs(gamma) * abs(shftdir - z)

        for y in range(image.height()):
            shift = lnshift(y)
            for x in range(image.width()):
                rgb = SpriteEditor.getpixel(image, x, y)
                if rgb != (0, 0, 0):
                    SpriteEditor.setpixel(newimag, int(x + shift), y, *rgb)
        return newimag

    @staticmethod
    def shearImageY(image, gamma):
        xresize = image.width()
        yresize = int(image.height() * (abs(gamma) + 1))
        newimag = PhotoImage(width=xresize, height=yresize)
        shftdir = {True: 0, False: image.width()}[(gamma < 0)]
        lnshift = lambda z: abs(gamma) * abs(shftdir - z)
        for x in range(image.width()):
            shift = lnshift(x)

            for y in range(image.height()):
                rgb = SpriteEditor.getpixel(image, x, y)
                if rgb != (0, 0, 0):
                    SpriteEditor.setpixel(newimag, x, int(y + shift), *rgb)
        return newimag

    @staticmethod
    def _resize(image, x=1, y=1):
        """Resizes and image"""
        assert isinstance(image, PhotoImage), 'incorrect type of arg image: should be type PhotoImage, is type {}'.format(type(image))
        return image.zoom(x, y=y)

    @staticmethod
    def getpixel(image, x, y):
        r, b, g = [ int(i) for i in image.get(x, y).split(' ') ]
        return r, b, g

    @staticmethod
    def setpixel(image, x, y, r, g, b):
        """Change image pixel to color r, b, g"""
        hexcode = "{#%02x%02x%02x}" % (r, g, b)
        image.put(hexcode, to=(x, y))

    def fill(self):
        """Fill image with a color=(r,b,g)
        Unused
        """
        r, g, b = (self.red.get(), self.green.get(), self.blue.get())
        width = self._image.width()
        height = self._image.height()
        hexcode = "#%02x%02x%02x" % (r, g, b)
        horizontal_line = "{" + " ".join([hexcode] * width) + "}"
        self._image.put(" ".join([horizontal_line] * height))

    @staticmethod
    def _shadeimg(image, shade=0):
        assert isinstance(image, PhotoImage), 'incorrect type of arg image: should be type PhotoImage, is type {}'.format(type(image))
        shade = 1 - (shade / 100.0)
        image = image.copy()
        
        for x in range(image.width()):
            for y in range(image.height()):
                s = map(lambda i: int(i), image.get(x, y).split(' '))
                s = map(lambda i: int(i * shade), s)
                hexcode = "#%02x%02x%02x" % tuple(s)
                image.put("{%s}" % (hexcode), to=(x, y))
        return image

class SpriteLoader():
    """Mix in for loading spritesheets, split for readablility"""
    def InferSpritesheetInfo(self, SpritesheetDict):
        SpritesheetDict.pop('xsize', None)
        SpritesheetDict.pop('ysize', None)
        xsize = max([ coord[0] for coord in SpritesheetDict.values() ]) + 1
        ysize = max([ coord[1] for coord in SpritesheetDict.values() ]) + 1
        return [xsize, ysize, SpritesheetDict]

    def ReadSpritesheetInfo(self, SpritesheetDict):
        xsize = SpritesheetDict.get('xsize', None)
        ysize = SpritesheetDict.get('ysize', None)
        return [xsize, ysize]

    def SpritesheetInfo(self, SpritesheetDict):
        r = self.ReadSpritesheetInfo(SpritesheetDict)
        i = self.InferSpritesheetInfo(SpritesheetDict)
        return [ r[n] or i[n] for n in range(2) ] + [ i[2] ]

    def blank(self):
        return { ImageName.str('blank'): PhotoImage(master=tk) }

    def missing_tex(self):
        try: 
            return { 'missing_texture': PhotoImage(master=tk, file='./media/spritesheets/missing_texture.gif') }

        except Exception as e:
            return { 'missing_texture': PhotoImage(master=tk) }

    def loadSpritesheet(self, name):
        #image = None
        #try:
        image = PhotoImage(master=tk, file='./media/spritesheets' + name)
        #except Exception as e:
        #    image = self.baseImages['missing_texture']
        #finally:
        return image

    def subimage(self, spritesheet, l, t, r, b):
        img = PhotoImage()
        img.tk.call(img, 'copy', spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return img

    def load_sprites(self, name, info):
        imges = {}
        sheet = self.loadSpritesheet(name)
        rdata = self.SpritesheetInfo(info)
        sdata = rdata[2]
        width = sheet.width() / rdata[0]
        height = sheet.height()/ rdata[1]
        for s in spriteinfo:
            try:
                l = int(spdata[s][0] * width )
                t = int(spdata[s][1] * height)
                r = int(l + width )
                b = int(t + height)
                imges.update( { str(ImageName(s)): self.subimage(sheet, l, t, r, b) } )
                
            except Exception as e:
                imges.update( { str(ImageName(s)): self.baseImages['missing_texture'] } )#logit
                
        return imges

class SpriteDict(SpriteLoader, object):
    """Image Dictionary"""
    def __contains__(self, x):
        b = False
        x = str(x)
        b |= x in self.baseImages.keys()
        b |= x in self.editedImages.keys()
        return b

    def __getitem__(self, image):
        assert isinstance(image, str) or isinstance(image, ImageName), 'incorrect type of arg image: should be type str or ImageName, is type {}'.format(type(image))
        img = ImageName(s=image)
        if img in self:
            base = self.baseImages.get(str(image), None)
            edit = self.editedImages.get(str(image), None)
            return base or edit or 'missing_texture'

        else:
            imageInst = self.editImage(image)
            self.editedImages.update({str(image): imageInst})
            return imageInst

    def __init__(self):
        self.baseImages = {}
        self.editedImages = {}
        self.baseImages.update( self.missing_tex() )
        self.baseImages.update( self.blank() )
        for s in ReqImages:
            self.baseImages.update( self.load_sprites(s, ReqImages[s]) )

    def editImage(self, image):
        assert isinstance(image, ImageName), 'incorrect type of arg image: should be type ImageName, is type {}'.format(type(image))
        imageInst = self.getBaseImage(image).copy()
        imageInst = self._resize(imageInst, x=image.xsize, y=image.ysize)
        imageInst = self._shadeimg(imageInst, shade=image.shade)
        imageInst = self.rotateimg(imageInst, deg=image.rspin)
        return imageInst

    def getBaseImage(self, image):
        assert isinstance(image, ImageName), 'incorrect type of arg image: should be type ImageName, is type {}'.format(type(image))
        return self.baseImages.get(str(image.base()), self.baseImages['missing_texture'])
    
    def getResolution(self, name, xsize, ysize, rspin):
        img = ImageName(name=name, xsize=xsize, ysize=ysize)
        img = self[img]
        res = self.imageRes(img, rspin)
        return res

    
class _ImageDictionary():
    """Image handling class"""
    def __init__(self):
        self.used = []
        self.free = [ _canvas.create_image(tk_border, base_size[1]+tk_border, anchor='sw') for _ in range(maxSprites) ]

    def get(self):
        try:
            img = self.free.pop(0)
            self.used.append(img)
            _canvas.tag_raise(img)
            return img

        except IndexError:
            warnings.warn(Warning('Image dict out of images'))

    def release(self, image):
        imageIndex = self.used.index(image)
        self.used.pop(imageIndex)
        self.free.append(image)

#--------------------------------------------------------------------

class DormantImage(object):
    """Dormant image"""
    def __init__(self, x, y, image, layer=1):
        """Class constructer
        showx and show y are where the image will move to upon the function show
        """
        self.x = 0
        self.y = 0
        self.showx = x
        self.showy = y
        self.tag = None
        self.image = sprites[image]
        self.layer = layer

    def __del__(self):
        self.hide()
        super(DormantImage, self).__del__()  

    def active(self):
        return self.tag is not None

    def config(self, *args, **kwargs):
        _canvas.itemconfig(self.gtag(), *args, **kwargs)

    def gtag(self):
        """Get Tag"""
        if not self.active():
            warnings.warn(Warning('Attempted to get a DormantImage instance to do an action before activation'))
        else: 
            return self.tag

    def width(self):
        return self.image.width()

    def height(self):
        return self.image.height()

    def move(self, x, y):
        self.x += x
        self.y += y
        if self.active():
            _canvas.move(self.gtag(), x, -y)

    def moveTo(self, x, y, r=False):
        """r means return"""
        x_move = x - self.x
        y_move = y - self.y
        if not r:
            self.move(x_move, y_move)
        else:
            return [x_move, y_move]

    def update(self, image, sx=None, sy=None):
        if sx is not None: self.showx = sx
        if sy is not None: self.showy = sy
        self.image = sprites[image]
        if self.active():
            self.config(image=self.image) 

    def raiseTag(self):
        """Raises the tag of the image if active"""
        if self.active(): 
            _canvas.tag_raise(self.gtag())

    def show(self):
        if not self.active():
            self.tag = imageDict.get()
            self.raiseTag()
            self.config(image=self.image)
            self.moveTo(self.showx, self.showy)

    def hide(self):
        """Releases the image in use"""
        if self.active(): 
            self.moveTo(0, 0)
            self.config(image=PhotoImage())
            imageDict.release(self.gtag())
            self.tag = None

class ComplexImage(object):
    """Complex image mixin that makes moving multiple images easier"""
    def __init__(self):
        a = [
            ['layer', {'layer': 3}]
        ]
        for i in a:
            name, d = i
            if name not in self.__dict__:
                self.__dict__.update(d)

    def __del__(self):
        self.hide()
        super(ComplexImage, self).__del__()

    def move(self, x, y):
        for i in self.images: 
            i.move(x, y)
        self.x += x
        self.y += y

    def move_to(self, x, y, r=False):
        """r is return"""
        x_move = x - self.x
        y_move = y - self.y
        if r == False:
            self.x += x_move
            self.y += y_move
            for i in self.images: 
                i.move(x_move, y_move)
        else: 
            return (x_move, y_move)

    def layersort(self, x, y):
        if x.layer < y.layer: return 1
        elif x.layer > y.layer: return -1
        elif x.layer == y.layer: return 0

    def raiseTag(self):
        #if self.active:
        self.images.sort(cmp=self.layersort)
        for i in self.images: 
            i.raiseTag()

    def show(self):
        for i in self.images: 
            i.show()

    def hide(self):
        for i in self.images: 
            i.hide()

class Keyboard(object):
    instances = []
    keys = 'a'
    states = {
        'pressed': {
            True: 'held',
            False: 'pressed'
        },
        'letgo': {
            True: 'off',
            False: 'letgo'
        }
    }
    def __del__(self):
        Keyboard.instances.remove(self)
        super(Keyboard, self).__del__()
        
    def __init__(self, fhz=60):
        self.target = 1 // 60
        self.cache = { c: ['letgo', time.clock() + self.target] for c in keys } #FOR EACH KEY CREATE TIMER
        Keyboard.instances.update(self)

    def _updateKey(self, key, tipe):
        key, tipe = key
        if not(self.ispressed(key) or self.held(key)) and tipe == 'pressed':
            self.cache[key][0] = 'pressed'
            self.cache[key][1] = time.clock()

        elif not(self.isletgo(key) or self.isoff(key)) and tipe == 'released':
            self.cache[key][0] = 'letgo'
            self.cache[key][1] = time.clock()
            
    def delta(self, key):
        return time.clock() - self.cache[key][1] - self.target
           
    @staticmethod
    def updateKey(key):
        for i in Keyboard.instances:
            i._updateKey(*key)
    
    def ispressed(self, key):
        return self.state(key) == 'pressed'
    
    def isheld(self, key):
        return self.state(key) == 'held'
    
    def isoff(self, key):
        return self.state(key) == 'off'
    
    def isletgo(self, key):
        return self.state(key) == 'letgo'
    
    def state(self, key):
        s = self.cache[key][0]
        c = self.delta(key) > self.target
        return Keyboard.states[s][c]
    
    
class UserInput(object):
    def __init__(self):
        self.keyboard = Keyboard()
    
    def handleKeyPress(self, event):
        pass
        
    def handleKeyRelease(self, event):
        pass
        
        
            
class GuiBase(ComplexImage):
    """tkinter base gui module"""
    def __call__(self, objpath, call, *args, **kwargs):
        #try:
        objpath = objpath.split('.')
        
        if objpath[0] not in self.images and len(objpath) == 1:
            return self.__getattribute__(objpath[0])(*args, **kwargs)

        obj = self.getimage(self.images[obj], *objpath[1:])

        if call:
            obj(*args, **kwargs)
            self.layer()
        
        return obj

        #except Exception as e:
        #  warnings.warn(Warning('Gui error: %s, %s' % (str(objpath), str(e))))

    def getimage(self, obj, *args):
        for i in args:
            obj = obj.__getattribute__(i)
        return obj

    def __init__(self):
        """Class constructor"""
        global tk, imageDict, _canvas, sprites, app_width, app_height
        tk = Tk()
        self.canvas = Canvas(tk, width=base_size[0]+tk_border, height=base_size[1]+tk_border, takefocus=True)
        self.canvas.pack()
        _canvas = self.canvas
        sprites = SpriteDict()
        imageDict = _ImageDictionary()
        self.images = {}

    def destroy(self):
        tk.destroy()

    def layer(self):
        imgs = [ i for i in self.images.values() ]
        imgs.sort(cmp=self.layersort)
        for i in imgs: i.raiseTag()

    def canvas(self):
        return _canvas

    def update(self):
        self.layer()
        tk.update()
    
    def render(self):
        self.layer()
        tk.update_idletasks()
