"""
Handles input
"""


import os
import sys

if __name__ == '__main__':
  sys.path.append(os.path.abspath('../'))
  os.chdir('../')

from mixins.fileLS import FileLS
from gameobj.board import MapArea
from gameobj.entities import OverworldEntity
from gui import guiMain


keybindFile = './dat/tkinterKeybinds.json'
keybinds = FileLS.load(keybindFile, s='json')

class OverworldMode(object):
  """Overworld"""
  def __init__(self, arg):
    self.player = OverworldEntity()
    self.board = MapArea()
    
  def tick(self):
    #check keyboard
    #Move player
    #Move other entities
    #
    
class Main(object):
  def __init__(self):
    self.gui = guiMain.Gui()
    self.userinput = guiMain.UserInput(list(keybinds.values()))
    
  def start(self):
    """Starts the game"""
    self.bindKeys()
    self.bindButtons()
    guiMain.tk.after(16, func=self.tick)
    guiMain.mainloop()
    
  def bind(self, s, f):
    gui._canvas.bind_all(s, f)

  def bindKeys(self):
    l = ['KeyPress', 'KeyRelease']
    for k, v in keybinds.items():
      self.bind('<KeyPress-{}>'.format(k), self.userinput.keyPress)
      self.bind('<KeyRelease-{}>'.format(k), self.userinput.keyRelease)
    
  def bindButtons(self):
    self.bind('<Motion>', self.userinput.mouseMove)
    self.bind('<ButtonPress-1>', self.userinput.mousePress)
    self.bind('<ButtonRelease-1>', self.userinput.mouseRelease)
    #gui._canvas.bind_all('<Button2>', self.userinput)
    
  def tick(self):
    pass
    
  def destroy(self):
    try: 
      gui.destroy()

    except Exception:
      pass

  def handle(self, ginput):
    self.game.handle(ginput)
    
