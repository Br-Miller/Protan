"""File to add data to dat files

"""


import os
import sys
import json

data = {
    'entity': './dat/entity.dat',
    'terrain': './dat/terrain.dat',
}

if __name__ = '__main__':
    path = os.path.abspath('./../../')
    os.chdir(path)
    sys.path.append(path)
  
def addEntity(d):
    pass
  
def loadjson(filepath):
    pass
  
def loadData():
    d = {}
    for name, path in paths.keys():
        
    path.update(d)
