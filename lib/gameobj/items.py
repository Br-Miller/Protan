"""Item objects

This class handles items
"""


import os, sys
import types
import marshal
if __name__ == '__main__': 
  sys.path.append( os.path.abspath('./../') )
  os.chdir('./../')
from mixins.logger import log, logit

itemList = {}
itemFile = './dat/items.dat'


class _Item(object):
  """docstring for _Item"""
  def __init__(self, config):
    super(_Item, self).__init__()
    self.arg = arg
    


def Item(name):
  return itemDict[name]

def addAbility(ability):
  abilityList.update({ability.name: ability})

def saveEntities():
  l = itemList.copy().values()
  l = marshal.dumps(l)
  with open(entitiesFile, 'w+b') as f:
    f.write(l)

def loadItems():
  try:
    d = {}
    content = ''

    with open(itemFile) as f:
      content = marshal.load(f)

    for i in content:
      action = _Ability.fromDict(i)
      d.update({action.name: action})

    return d

  except Exception as e:
    log('Could not load abilities, %s' % (str(e)), logtype='e')
    raise
    return {}


entityList = loadItems()