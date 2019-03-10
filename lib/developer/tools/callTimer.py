"""Function call counter and timer

Timing how long modules take is important for testing
how efficient code is. It is also important to know 
how many times a function is being called. This 
module has code that can time how long it a function 
takes and how many times it is called. Only works for
classes. This behavior is intended to be changed
"""


from functools import wraps
from time import time
from types import FunctionType


class timeCallMeta(type):
  def __new__(meta, name, bases, class_dict): 
    avoidFunc = ['__init__', '__getattribute__', '__getattr__']

    for k, v in class_dict.items():
      if callable(v) and k not in avoidFunc and not isinstance(func, staticmethod):
        class_dict.update({k: meta.__decorate(v)})

      elif k == '__init__':
        class_dict.update({k: meta.__decorateInit(v)})

    return type.__new__(meta, name, bases, class_dict)

  @staticmethod
  def __decorateInit(func):
    @wraps(func)
    def decoratedFunc(self, *args, **kwargs):
      self.timeCallDict = {}
      return func(self, *args, **kwargs)
    return decoratedFunc

  @staticmethod
  def __decorate(func):
    @wraps(func)
    def decoratedFunc(*args, **kwargs):
      timeStart = time()
      output = func(*args, **kwargs)
      timeEnd = time()
      timeTotal = timeEnd - timeStart
      self = args[0]

      if func.__name__ not in self.timeCallDict.keys():
        self.timeCallDict.update({func.__name__: [1, timeTotal]})

      else:
        self.timeCallDict[func.__name__][0] += 1
        self.timeCallDict[func.__name__][1] += timeTotal
        self.timeCallDict[func.__name__][1] /= 2

      return output
    return decoratedFunc


class timeCallTest(object):
  """docstring for timeCallTest"""
  def __getattribute__(self, a):
    a = super(timeCallTest, self).__getattribute__(a)
    d = super(timeCallTest, self).__getattribute__('__dict__')

    if 'timeCallTestDict' not in d:
      self.timeCallTestDict = {}

    d = super(timeCallTest, self).__getattribute__('timeCallTestDict')

    if callable(a):
      def decoratedFunction(*args, **kwargs):
        timeStart = time()
        r = a(*args, **kwargs)
        timeEnd = time()

        if a.__name__ not in d:
          d.update({a.__name__: [1, timeEnd-timeStart]})

        else:
          d[a.__name__][0] += 1
          d[a.__name__][1] += timeEnd - timeStart
          d[a.__name__][1] /= 2

        return r
      return decoratedFunction
    return a
    