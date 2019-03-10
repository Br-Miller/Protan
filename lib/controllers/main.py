"""
Handles input
"""


import os
import sys

if __name__ == '__main__':
  sys.path.append(os.path.abspath('../'))
  os.chdir('../')

from gameobj.board import MapArea
from gameobj.entities import OverworldEntity
from gui import guiPlaceholder


keybindFile = './dat/tkinterKeybinds.json'


class OverworldMode(object):
  """Overworld"""
  def __init__(self, arg):
    self.player = entities()
    self.board = MapArea()
    
class main(object):
  """Main"""
  def __init__(self):
    global gui
    gui = guiPlaceholder.Gui()
    
  def start(self):
    """Starts the game"""
    f = open(keystrokesFile)
    keybinds = json.load(f)
    f.close()

    allKeys = {}
    l = ['lowercase', 'uppercase', 'functions', 'numbers', 'symbols']
    
    for i in l: 
      allKeys.update(keybinds[i])

    for key in allKeys:
      gui._canvas.bind_all(key, self.handle_ki) 
    gui._canvas.bind_all('<Button-1>', self.handle_rmsi)
    gui._canvas.bind_all('<Button-2>', self.handle_lmsi)
    gui._canvas.bind_all('<Motion>', self.handle_mi)
    guiPlaceholder.mainloop()

  def destroy(self):
    try: 
      gui.destroy()

    except Exception:
      pass

  def handle(self, ginput):
    self.game.handle(ginput)

  def handle_ki(self, pinput):
    """Handles player's key input"""
    input_data = ('Key', pinput.keysym)
    self.handle(input_data)

  def handle_mi(self, minput):
    """Handles player's mouse movement"""
    self.handle(('MouseMove', (minput.x - gui_module.tk_border, minput.y - gui_module.tk_border)))

  def handle_rmsi(self, minput):
    """Handles player's mouse's right single click's"""
    self.handle(('SRightPress', (minput.x - gui_module.tk_border, minput.y - gui_module.tk_border)))

  def handle_rmdi(self, minput):
    """Handles player's mouse's right double click's"""
    self.handle(('DRightPress', (minput.x - gui_module.tk_border, minput.y - gui_module.tk_border)))

  def handle_lmsi(self, minput):
    """Handles player's mouse's left single click's"""
    self.handle(('SLeftPress', (minput.x - gui_module.tk_border, minput.y - gui_module.tk_border)))

  def handle_lmdi(self, minput):
    """Handles player's mouse's left double click's"""
    self.handle(('DLeftPress', (minput.x - gui_module.tk_border, minput.y - gui_module.tk_border)))

  def handle_mwi(self, minput):
    """Handles player's mousewheel"""
    self.handle(('MouseWheel', (minput.x, minput.y)))