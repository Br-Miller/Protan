"""
Tool for creating abilities
"""


if __name__ != '__main__':
  raise Exception('This module should not be imported!')

import os, sys
if __name__ == '__main__': 
  import os, sys
  sys.path.append( os.path.abspath('./../../') )
  os.chdir('./../../')
from gameobj.entities import _Ability, addAbility, saveAbilities


def returnExec(x):
  exec('a = %s' % (x))
  return a


def askUntilValid(s, valid=lambda x: True):
  k = None

  while not valid(k):
    k = raw_input(s)

  return k

def isInt(i):
  if isinstance(i, int):
    return True

  else:
    try:
      int(i)
      return True

    except Exception as e:
      return False


def createAbility():
  d = {'y': True, 'n': False}
  askStr = lambda i: isinstance(i, str)
  askInt = lambda i: isInt(i)
  askBool = lambda s: s == 'y' or s == 'n'
  askTarget = lambda s: sum([ s == i for i in ['all', 'ally', 'enemy', 'self']]) == 1
  
  name = askUntilValid('What is this abilities name? ', askStr)
  ta1 = askUntilValid('What does this ability target? (all, ally, enemy, self) ', askTarget)
  ta2 = askUntilValid('Does this ability target all the entities in the set? (y/n) ', askBool)
  ta3 = askUntilValid('Can this ability target dead entities? (y/n) ', askBool)
  c1 = askUntilValid('How much health does this cost? ', askInt)
  c2 = askUntilValid('How much mana does this cost? ', askInt)
  tb1 = askUntilValid('What type of damage is this? ')
  tb2 = askUntilValid('What type of healing is this? ')
  a1 = askUntilValid('How is the damage calculated? ', askStr)
  a2 = askUntilValid('How is the heal calculated? ', askStr)
  a1 = returnExec('lambda e: %s' % (a1))
  a2 = returnExec('lambda e: %s' % (a2))

  l = [
    name,
    {
      'target': ta1, 
      'all': d[ta2], 
      'alive': not d[ta3],
    },
    {
      'hp': c1,
      'mp': c2,
    },
    {
      'damage': tb1,
      'heal': tb2,
    },
    {
      'damage': a1,
      'heal': a2,
    },
  ]
  addAbility(_Ability(*l))

def updateFile():
  saveAbilities()