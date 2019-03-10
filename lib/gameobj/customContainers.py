"""Custom Container Classes

This module contains custom container classes to increase efficiency
and decrease memory usage
"""

import os, sys
if __name__ == '__main__': 
  sys.path.append( os.path.abspath('./../') )
  os.chdir('./../')
from helpers.miniHelpers import flatten


class info_class(object):
  """Class that creates its variables from a dictionary"""
  def __init__(self, dictionary):
    self.__dict__ = dictionary


class compactMatrix(dict):
  """Custom dictionary matrix class that decreases memory usage
  When getting a non-existant key, returns r
  Does not have to be a matrix
  """
  def __init__(self, d={}, r=None):
    """Class constructor"""
    self.r = r
    super(compactMatrix, self).__init__(d)
  
  def __getitem__(self, k):
    """Customised getitem function"""
    try:
      return super(compactMatrix, self).__getitem__(k)

    except KeyError:
      return self.r


class compactValueDict(dict):
  """Compact dictionary class that saves memory space
  Saves values as keys and keys in lists
  Should be used when values are repetitive but keys are not
  compactMatrix({'a':'b', 'c':'d', 'e': 'b'}) -> {'b': ['a', 'e'], 'd': ['c']}
  """
  def __getitem__(self, i):
    """Customised getitem function
    Looks through values to find i, and if found, returns it's key
    """
    for k, v in self.items():
      if i in v:
        return k
    return self.r

  def __init__(self, d={}, r=None):
    """Class constructor"""
    self.r = r
    d = self.convertTo(d)
    super(compactValueDict, self).__init__(d)

  def sortValues(self):
    for _, v in self.items():
      v.sort()

  def _multiPop(self, l):
    """Internal function
    More efficient version of pop that pops multiple items at a time
    """
    for k, v in self.items():
      for i in l:
        if i in v:
          v.remove(i)

  def convertFrom(self, d=None):
    """Converts a dictionary from this classes format back into the original format
    If d is None, the dictionary to be edited defaults to this class
    """
    d = d or self
    d = d.copy()
    newDict = {}
    
    for k, v in d.items():
      for i in v:
        newDict.update({i: k})

    return newDict

  @staticmethod
  def convertTo(d):
    """Converts a dictionary into this classes format"""
    newDict = {}

    for k, v in d.items():
      if v not in newDict.keys():
        newDict.update({v: [k]})

      elif v in newDict.keys():
        newDict[v].append(k)

    return newDict

  def pop(self, i):
    """Pops a key (value)"""
    for k, v in self.items():
      if i in v:
        return v.remove(i)
    return None

  def remove(self, k):
    """Removes a key (value)"""
    super(compactValueDict, self).pop(k)

  def update(self, d):
    """Updates this dictionary
    d should NOT be in this classes format
    """
    d = self.convertTo(d)
    allValues = flatten(d.values())
    self._multiPop(allValues)

    for k, v in d.items():
      if k in self: 
        super(compactValueDict, self).__getitem__(k).extend(v)

      else: 
        super(compactValueDict, self).update({k: v})


class KeyBoardLine(str):
  """Keyboard line object"""
  def __call__(self, input):
    if iType == 'Key':
      if iInfo == 'BackSpace':
        self.string = self.string[:-1]

      elif iInfo == 'Return':
        return self.string

      elif len(iInfo) == 1:
        self.string += iInfo

      elif iInfo in symbol_str:
        self.string += symbol_str[iInfo]


class PseudoInfinity(object):
  """docstring for PseudoInfinity"""
  def __str__(self):
    return 'PseudoInfinity'

  def __le__(self, *args):
    return True

  def __ge__(self, *args):
    return True

  def __gt__(self, *args):
    return True

  def __lt__(self, *args):
    return True

  def __eq__(self, *args):
    return False

  def __gt__(self, *args):
    return True


class InfiniteRange(object):
  """docstring for Infinite Range
  None is considered infinity"""
  def __contains__(self, n):
    assert isinstance(n, int), "incorrect type of arg n: should be type int, is type {}".format(type(n))
    return self.rmin <= n < self.rmax

  def __init__(self, rmin=None, rmax=None):
    self.rmin = rmin or PseudoInfinity()
    self.rmax = rmax or PseudoInfinity()
    super(InfiniteRange, self).__init__()

  def __repr__(self):
    return repr((self.rmin, self.rmax))

  def __str__(self):
    return str((self.rmin, self.rmax))

    
    