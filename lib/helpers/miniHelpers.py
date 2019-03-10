"""Helper functions

Module that contains helper functions that are too
small to go into other modules
"""


def flatten(l):
  """Flattens a list
  [[1, 2], [3, 4], [5, 6]] -> [1, 2, 3, 4, 5, 6]
  """
  newl = []
  for i in l:
    if isinstance(i, list):
      i = flatten(i)
      newl.extend(i)
    else:
      newl.append(i)
  return newl

def loop(n, nMin, nMax=None, loop=True):
  nMax = nMax or 0
  l = [nMin, nMax]
  nMin = min(l)
  nMax = max(l)
  d = {
    (True, False, True): nMax,
    (False, True, True): nMin,
    (False, False, True): n,
    (True, False, False): nMin,
    (False, True, False): nMax,
    (False, False, False): n,
  }
  return d[(n < nMin, n >= nMax, loop)]