"""Main game controller

The main controller for the game
"""


#Standard Imports
import string
from threading import *
from queue import PriorityQueue
from warnings import warn

#Other Imports
import pygame
pygame.init()
from helpers.modification import loop

#Global constants
running = False
debugMode = False
inputQueue = PriorityQueue(maxsize=10)


class RawInputHandler(thread):
  """docstring for rawInputHandler"""
  def __init__(self):
    self.doned = arg
    super().__init__()

  def run(self):
    t = Timer(0.017, f, args=[], kwargs={})
    t.start()
    while running: #Change to active
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          done = True

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            player.go_left()
          if event.key == pygame.K_RIGHT:
            player.go_right()
          if event.key == pygame.K_UP:
            player.jump()

        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LEFT:
            player.stop()
          if event.key == pygame.K_RIGHT:
            player.stop()

  def processInput(self):
    self.checkKeys()
    self.cleanup()
    

class UserKeyboard(dict):
  """docstring for PlayerKeyboard"""
  keys = [ c for c in '`1234567890-=abcdefghijklmnopqrstuvwxyz[]\\;\',./ ' ] + ['enter', 'rshift', 'lshift', 'tab', 'escape', 'upArrow', 'downArrow', 'leftArrow', 'rightArrow']
  states = ['pressed', 'held', 'released', 'off']
  defaultKeyBindings = {
    #Global
    'up': 'upArrow',
    'down': 'downArrow',
    'left': 'leftArrow',
    'right': 'rightArrow',
    'menu': 'enter',
    #During Platforming
    'jump': 'z',
    'interact': 'c',
    #During Menu
    'select': 'z',
    'back': 'x',
  }
  def __init__(self, keybindings):
    self.keybindings = keybindings
    super().__init__()

  def __getitem__(self, key):
    if key in self.keyBindings.keys():
      key = self.keybindings[key]

    if key not in self:
      return UserKeyboard.states[3]
    return super().__getitem__(key)

  def checkKeys(self):
    d = {
      states[1]: states[1],
      states[0]: states[1],
      states[2]: states[4],
    }
    newd = { k: d[v] for k, v in self.items() }
    self.update(newd)

  def cleanup(self):
    """Cleans up keys in the off state"""
    for k, v in self.items():
      if v == state[3]:
        self.remove(k)

  def isHeld(self, key):
    """Whether the key is being held"""
    return self.isState(key, UserKeyboard.states[1])

  def isPressed(self, key, strict=True):
    """Whether the key is pressed"""
    held = self.isState(key, UserKeyboard.states[1])
    pressed = self.isState(key, UserKeyboard.states[0])
    d = {True: pressed, False: held or pressed}
    return d[strict]

  def isReleased(self, key):
    """Whether the key is released"""
    return self.isState(key, UserKeyboard.states[2])

  def isState(self, key, state):
    """Whether the key is in the state given"""
    assert isinstance(state, str), "incorrect type of arg state: should be str, is {}".format(type(state))
    assert isinstance(key, str), "incorrect type of arg key: should be str, is {}".format(type(key))
    assert state in UserKeyboard.states, "expected button state: got {}".format(state)
    assert key in UserKeyboard.keys, "expected keyboard button: got {}".format(key)
    return self[key] == state

  def pressedKeys(self):
    """Returns an dictionary of the currently pressed, held or released keys"""
    warn(PendingDeprecationWarning('This module is pending a change'))
    self.cleanup()
    return self.keys()


class TurnFightActionMenu(object):
  """docstring for TurnFightActionMenu"""
  def __init__(self, ):
    self.arg = arg
    super().__init__()


class TurnFight(object):
  """docstring for TurnFight"""
  def __init__(self, playerParty, enemyParty, advantage='player'):
    assert isinstance(playerParty, list), "incorrect type of arg playerParty: should be type list, is {}".format(type(playerParty))
    assert isinstance(enemyParty, list), "incorrect type of arg enemyParty: should be type list, is {}".format(type(enemyParty))
    assert isinstance(advantage, str), "incorrect type of arg advantage: should be type str, is {}".format(type(advantage))

    self.parties = {
      'enemy': enemyParty,
      'player': playerParty,
    }
    self.mode = 'selectingAlly'
    self._highlight = 0
    self.selecting = None
    self.turn = advantage
    super().__init__()

  def currentParty(self):
    """Returns a list of the current turns entities"""
    return self.parties[self.turn]

  def handleEnemies(self):
    """Handles all the enemies in the enemies list"""
    assert self.turn == 'enemy', "expected current turn to be enemy: is {}".format(self.turn)
    
    for entity in self.currentParty():
      if self.hasLost('player'):
        break

      try:
        entity.decide()

      except Exception as e:
        #Log error, continue
        pass

    self.nextTurn()


  def handleInput(self, userInput):
    """Handles the player input"""
    assert isinstance(userInput, UserKeyboard), "incorrect type of arg userInput: should be type UserKeyboard, is {}".format(type(userInput))

    if self.mode == 'selectingAlly':
      if userInput.isPressed('up', strict=True):
        self.shiftHighlight('up')

      if userInput.isPressed('down', strict=True):
        self.shiftHighlight('down')

      if userInput.isPressed('select', strict=True): 
        self.mode = 'selectingAbility'
        self.selecting = 0

    elif self.mode = 'selectingAbility':
      if userInput.isPressed('up', strict=True):
        self.shiftSelecting('up')

      if userInput.isPressed('down', strict=True):
        self.shiftSelecting('down')

    if self.turn == 'enemy':
      self.handleEnemies()

  def shiftHighlight(self, direction):
    d = {'up': -1, 'down': 1}
    i = d[direction]
    b = 0
    self.highlight += i

    while not self.highlightValid():
      b += 1
      self.highlight += i

      if b > 20:
        break

    return

  def hasLost(self, party):
    """Returns whether the party stated has lost"""
    return not self.isAlive(party)

  def hasWon(self, party):
    """Returns whether the party stated has won"""
    return not self.isAlive(party)

  def highlightValid(self):
    entity = self.parties['player'][self.highlight]
    return entity.alive() and entity.canAction

  def highlightValid(self):
    entity = self.parties['player'][self.highlight]
    return entity.alive() and entity.canAction

  def isAlive(self, party):
    """Returns if the at least one of entities in the party listed are alive"""
    assert isinstance(party, str), "incorrect type of arg party: should be type str, is {}".format(type(party))
    assert party in self.parties.keys(), "expected arg party to be a party: is {}".format(party)

    l = self.parties[party]
    l = map(lambda e: e.alive(), l)
    l = reduce(lambda x, y: x & y, l)
    return l

  def nextTurn(self):
    """Switches the turn to the other party"""
    d = {
      'enemy': 'player',
      'player': 'enemy',
    }
    self.turn = d[self.turn]
    [ e.turnStart() for e in self.currentParty() ]

  def render(self):
    """Renders the updates in the turn"""
    pass

  def renderAction(self):
    pass

  @property
  def highlight(self):
    return self._highlight

  @highlight.setter
  def highlight(self, n):
    n = loop(n, len(self.party['player']), loop=True)
    self._highlight = n

  @property
  def selecting(self):
    return self._highlight

  @selecting.setter
  def selecting(self, n):
    n = loop(n, len(self.party['player'][self.highlight].abilities)+2, loop=True)
  

class SpeechMode(object):
  """Speech class to handle talking"""
  def __init__(self, arg):
    super().__init__()
    self.arg = arg


class PlatformMode(object):
  """docstring for PlatformMode"""
  def __init__(self, arg):
    super().__init__()
    self.arg = arg


class Main(object):
  """docstring for Main"""
  def __init__(self, arg):
    super(Main, self).__init__()
    self.arg = arg  