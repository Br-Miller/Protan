"""
NEWGAMENAME
Version 0.0.0.1

This is the game loading module. This module loads the game
as well as the configuration settings.

All modules contained in this game within the lib directory 
assume that upon import, the current filepath is ./NEWGAME/lib.
"""


import json
import os, sys
import platform
from importlib import import_module

gameName = 'Name'
version = '0.0.0.1'
developedBy = 'Name'
formatHeader = '%s\nVersion: %s\nDeveloped By: %s' % (gameName, version, developedBy)
configFile = os.path.join('.', '..', 'config', 'settings.json')
libFilepath = os.path.join('.', '..', 'lib')
configDefault = { #Default configuration settings
  #sound settings
}


def newConfigFile(s):
  with open(configFile, 'w') as f:
    logger.log(s + ', generating new config file', logtype='e')
    s = json.dumps(configDefault, sort_keys=True, indent=2, separators=(': ', ', '))
    f.write(s)
  return configDefault

def readConfig():
  content = None

  try:
    with open(configFile) as f:
      content = json.loads(f)

  except IOError: #File couldn't be opened
    content = newConfigFile('Missing config file')

  except TypeError: #File couldn't be
    content = newConfigFile('Config file was corrupted')

  except Exception: #File couldn't be
    content = newConfigFile('A strange error occurred while loading the config file')

  else:
    for k, v in configDefault:
      content.setDefault(k, v)

  finally:
    return content


def main():
  game = None
  exceptionRaised = False

  try:
    global logger
    sys.path.append(os.path.abspath(libFilepath))
    os.chdir(libFilepath)

    logger = import_module('mixins.logger')
    logger.log('Game Name   : {}'.format(gameName))
    logger.log('Version No  : {}'.format(version))
    logger.log('Platform    : {}'.format(platform.platform()))
    logger.log('  Release   : {}'.format(platform.release()))
    logger.log('  Version   : {}'.format(platform.version()))
    logger.log('Developed By: {}'.format(developedBy))
    logger.log('Reading configuration settings')

    config = readConfig()
    game = import_module('controllers.main')
    #gameInst = game.main()
    #gameInst.start()

  except ImportError, e: #A module is missing
    logger.log('Missing a module or error during import: {}'.format(e), logtype='e')
    exceptionRaised = True

  except IOError, e: #Invalid Filepath
    logger.log('Invalid filepath, {}'.format(e), logtype='e')
    exceptionRaised = True

  except Exception, e: #Unknown Exception
    logger.log('An unknown exception has occured: {}'.format(e), logtype='e')
    exceptionRaised = True

  finally:
    if exceptionRaised and game == None:
      logger.log('The game crashed before it opened. An issue is afoot', logtype='e')

    elif exceptionRaised:
      generateCrashReport(game)

    else:
      game.destroy()


if __name__ == '__main__':
  main()

sys.exit(0)