"""Custom input and output formatting

"""


import os
from formatter import *


class formatFilepath():
  """Formats filepaths into the correct format"""
  sep = os.path.sep
  @staticmethod
  def formatFilepath(s):
    s = s.split('\\')
    s = '/'.join(s)
    s = s.split('/')
    s = formatFilepath.sep.join(s)
    return s


class formattedStr(str):
  """Custom class that adds font to string
  Not efficient class, to be edited later
  """
  def __init__(self, s=''):
    self.formats = {}
    super().__init__(s)

  def font(self, index):
    pass

#Font uses dictionary with custom indexes