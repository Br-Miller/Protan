"""String Formatting Stuff

"""


import re


class strFormat(): #RECREATE
  """String formatting mixin

  Methods:

  _wsplit(...)   -- Splits a string at the spaces
  __dir(...)     -- Returns a generalised direction from variations of the direction
  sf_align(...)  -- Aligns a string in a certain direction
  sf_cstrip(...) -- Strips a string of all whitespaces
  sf_hyphen(...) -- Not Implemented
  sf_length(...) -- Not Implemented
  sf_stat(...)   -- Formats a string to neatly display a stat
  """
  def sf_align(self, s, slen, align_dir):
    """Aligns a string in a certain direction
    
    Args:
      s: String to be formatted
      slen: Desired string length
      align_dir: Direction to be aligned in (left, right or mid)
      bias: If the no of filler spaces is odd and align_dir is mid, 
            the biased section will have the extra spaces
    """
    if len(s) > slen: raise FormatLengthError('String is bigger than desired length')
    align_dir = self.__dir(align_dir)
    if align_dir == 'mid':
      s = s.strip().center(slen)
    elif align_dir == 'right': 
      s = s.rjust(slen)
    elif align_dir == 'left':
      s = s.ljust(slen)
    return s

  def sf_stat(self, s, n, slen):
    """Formats a string to neatly display a stat

    Will display the stat as s + : + n and the number will be aligned to the right
    """
    n = str(n)
    s += ':'
    fspace=slen - len(n + s)
    deslen=fspace + len(n)
    n = self.sf_align(n, deslen, 'right')
    s += n
    return s

  def sf_cstrip(self):
    """Strips a string of all whitespaces"""
    s = s.split(' ')
    return ''.join(s)

  def __dir(self, d):
    """Returns a generalised direction from variations of the direction

    Supports only the words left, right and middle
    Defaults to left
    """
    d = d.lower().strip()
    mid = ['mid',   'm', 'middle', '0', 'centre']
    left = ['left',  'l', 'left'  , '-1']
    right = ['right', 'r', 'right' , '1' ]
    dirs = [mid, left, right]
    for x in dirs:
      if d in x: return x[0]
    return 'left'

  def sf_fill(self, s, fill=[], filler=''):
    for i in fill: s = s.replace(i, filler)
    return s

  def sf_FitLen(self, s, maxlen):
    if len(s) > maxlen: s = s[:maxlen] 
    if len(s) < maxlen: s = s.ljust(maxlen)
    return s

  def _SentenceFit(self, a, maxlen, height):
    warnings.warn(DeprecationWarning('_SentenceFit function is outdated'))
    if len(a) > height: a = a[:height]
    if len(a) < height: a += [ ' '*maxlen for _ in range( height - len(a)) ]
    return a

  def sf_fit_sentence(self, s, maxlen, height, splitchar='\n'):
    a=s.split(splitchar)
    if len(a) > height: a = a[:height]
    if len(a) < height: a += [ ' ' * maxlen for _ in range( height - len(a)) ]
    return a

  def sf_multiformat(self, s, length, fill=[], filler='', align='left'):
    s = self.sf_fill(s, fill=fill, filler=filler)
    s = self.sf_FitLen(s, length)
    s = self.sf_align(s, length, align_dir=align)
    return s

  def sf_sentence(self, s, maxlen, splitchars=[' ']):
    if len(s) <= maxlen:
      return s
    l=[ i for i, x in enumerate(s) if x in splitchars ]
    #Find the largest index of split char that is smaller than maxlen
    n = 0
    for i in l:
      if i <= maxlen:
        n = i
      elif i > maxlen:
        break
    #Split at n
    l = s[:n]
    r = s[n+1:]
    r = self.sf_sentence(r, maxlen, splitchars=splitchars)
    l += '\n%s' % (r)
    return l

  def sf_allcapitalise(self, s, splitchar=' '):
    """Capitalises all"""
    s = s.split(splitchar)
    l = [ i.capitalize() for i in s ]
    return splitchar.join(l)