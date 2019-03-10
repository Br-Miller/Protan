"""
Logger that logs all the info that happens in order to identify bugs
more efficiently
"""


import os
import glob
from warnings import *
from datetime import datetime


max_logs = 12
current_log = None
log_filepath = None


def clear_logs():
  logs = glob.glob(os.path.abspath('./logs/*.txt'))
  logs.sort()
  if len(logs) > max_logs - 1:
    excess = len(logs) - max_logs + 1
    for i in range(excess):
      f = logs.pop(0)
      print(f)
      os.remove(f)

def newlog():
  """Creates a new log"""
  global log_filepath, current_log
  checkLog()
  clear_logs()
  log_filepath = os.path.abspath('./logs')
  s = str(datetime.now())
  s = log_filepath + '/' + s[:19].replace(':', '.') + '.txt'
  f = open(s, 'w+')
  f.close()
  current_log = s

def log(s, logtype='g'):
  """Logs info"""
  d = { 'g': 'General', 'e': 'Error' }
  info = '%s; %s: %s\n' % (str(datetime.now()), d[logtype], s)

  if logtype == 'e':
    warn(Warning(s))

  with open(current_log, 'a') as f: 
    f.write(info)

def checkLog():
  if current_log is None or log_filepath is None:
    newlog()