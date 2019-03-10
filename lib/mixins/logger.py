"""Logging module

Logger module that logs information into a predefined file
"""


import os
import glob
import random
import marshal
from datetime import datetime
from functools import wraps
from pickle import Pickle
from time import time
from warnings import *


maxLogs = 6
debugMode = False
crashFlav = []
currentLog = None
logFilePath = os.path.join('.', 'logs')
logExtension = 'txt'
logTypesDict = {'g': 'General', 'e': 'Error', 't': 'Time'}
crashFlavpath = os.path.join('.', 'dat', 'crashText.dat')
maxLogTypeLen = max(map(lambda v: len(v), logTypesDict.values()))


def setDebug():
  global debugMode
  debugMode = True


def loadCrashFlav():
  with open(crashFlavpath) as f:
    global crashFlav
    crashFlav = marshal.load(f)


def addCrashFlav(flav):
  with open(crashFlavpath, 'w+b') as f:
    crashFlav.append(flav)
    marshal.dump(crashFlav, f)


def cleanupLogs():
  """Automatically cleans up logs to save memory
  Clears logs when log number is over maxLogs
  """
  logs = os.path.join(logFilePath, '*.%s' % (logExtension))
  logs = os.path.abspath(logs)
  logs = glob.glob(logs)
  logs.sort()
  if len(logs) > maxLogs - 1:
    excess = len(logs) - maxLogs + 1
    for i in range(excess):
      f = logs.pop(0)
      print(f)
      os.remove(f)


def newLog():
  """Creates a new log
  The new logs name is the current date and time
  """
  global currentLog
  cleanupLogs()
  logPath = os.path.abspath(logFilePath)
  logFileName = str(datetime.now())[:19].replace(':', '.') + '.%s' % (logExtension)
  logPath = os.path.join(logPath, logFileName)
  currentLog = logPath
  f = open(currentLog, 'w+')
  f.close()


def filterLog(logFile, exclude=[]):
  content = None
  filteredLog = []

  with open(logfile) as f:
    content = f.read()
    content = content.split('\n')

  for l in content:
    for e in exclude:
      if logTypesDict[e] not in l[:28 + maxLogTypeLen]:
        filteredLog.append(l)

  return filteredLog


def logit(func, logtype='g', logtime=False, debug=debugMode):
  """Decorator to automatically log when a function is called"""
  @wraps(func)
  def logWrappedFunc(*args, **kwargs):
    try:
      a = time()
      result = func(*args, **kwargs)
      b = time()

      logGeneral = '%s was called with args %s and kwargs %s' % (func.__name__, str(args), str(kwargs))
      log(logGeneral, logtype=logtype)
      
      if logtime and debug:
        logTime = '%s was called and took %.6fs to resolve' % (func.__name__, b - a)
        log(logTime, logtype='t')

      return result

    except Exception as e:
      logError = 'failed to call %s with args %s and kwargs %s, (%s)' % (func.__name__, str(args), str(kwargs), str(e))
      log(logError, logtype='e')

  return logWrappedFunc


def log(s, logtype='g'):
  """Logs the info given

  Args:
    s: The information to be logged
    logtype: The log type, can be g[eneral] or e[rror]
  """
  assert isinstance(s, str), "incorrect type of arg s: should be str, is {}".format(type(s))
  assert isinstance(logtype, str), "incorrect type of arg logtype: should be str, is {}".format(type(logtype))

  info = '%s; %s: %s\n' % (str(datetime.now()), logTypesDict[logtype], s)
  with open(currentLog, 'a') as f: f.write(info)


class CrashReport(object):
  """Generates a crash report"""
  def __init__(self, game, header):
    self.game = game
    self.header = header

  def generate(self):
    crashFilepath = os.path.join(logFilePath, 'crash' + str(datetime.now()) + '.txt')
    
    with open(crashFilepath, 'w') as f:
      pass

  def inferError(self):
    pass

  def gameInstance(self):
    pass


if currentLog == None:
  newLog()