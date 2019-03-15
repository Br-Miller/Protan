"""Impact objects
Based off impact
"""


import random
import time


class Clock(object):
  """Clock object that keeps clocking time the same"""
  def __call__(self):
    """Pauses the clock for the time remaining till the next tick"""
    deltat = time.clock() - self.last
    deltas = max([0, target - deltat])
    time.sleep(deltas)
    self.last = time.clock()

  def __init__(self, seconds):
    self.last = time.clock()
    self.target = seconds

class Timer():
  """Counts how many seconds pass"""
  def __init__(self, frames=0):
    self.base = time.clock()
    self.last = time.clock()
    self.target = frames
    self.pausedAt = 0

  def set(self, t=0):
    self.target = t
    self.base = time.clock()
    self.pausedAt = 0

  def reset(self):
    self.base = time.clock()
    self.pausedAt = 0

  def tick(self):
    delta = time.clock() - self.last
    self.last = time.clock()
    return None #(self.pausedAt ? 0 : delta) #WHAT IS THIS

  def delta(self):
    return (self.pausedAt or time.clock()) - self.base - self.target

  def pause(self):
    if not self.pausedAt:
      self.pausedAt = time.clock()

  def unpause(self):
    if self.pausedAt:
      self.base += time.clock() - self.pausedAt
      self.pausedAt = 0

class Animation():
  """docstring for Animation"""
  def __init__(self, frameTime, sequence, stop=True):
    """Class constructor
    frameTime is how many frames before the next image
    """
    self.timer = Timer()
    self.frameTime = frameTime / 60.0
    self.sequence = sequence
    self.stop = stop
    self.tile = self.sequence[0]
    self.loopCount = 0

  def rewind(self):
    self.timer.set()
    self.loopCount = 0
    self.tile = self.sequence[0]

  def gotoFrame(self, frame):
    self.timer.set(self.frameTime * -f)
    self.update()

  def gotoRandomFrame(self):
    self.gotoFrame(int(random.random() * len(self.sequence)))

  def update(self):
    frameTotal = int(self.timer.delta() / self.frameTime)
    self.loopCount = int(frameTotal / len(self.sequence))

    if not self.stop and self.loopCount > 0:
      self.frame = len(self.sequence) - 1
    else:
      self.frame = frameTotal % len(self.sequence)

    self.tile = self.sequence[self.frame]

