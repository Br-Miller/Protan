"""Module to add data to data files"""


import os
import sys
import json
from warnings import warn

path = {
    'entity': './dat/entity.dat',
    'terrain': './dat/terrain.dat',
}
data = {}

if __name__ = '__main__':
    path = os.path.abspath('./../../')
    os.chdir(path)
    sys.path.append(path)
  

def addEntity(d):
    pass

def dumpjson(filepath, x):
    with open(filepath, 'w') as f:
        x = json.dumps(x)
        f.write(x)

def loadjson(filepath):
    try:
        f = open(filepath)
        c = f.reads()
        c = json.loads(c)
        f.close()
        return c
    except IOError:
        dumpjson(filepath, {})
        return {}

def saveData():
    for k, v in path.items()
        dumpjson(v, data[k])
    
def loadData():
    d = {}
    for k, v in path.items():
        d.update({k: loadjson(v)})
    data.update(d)
    
def nullfunction():
    pass
    
def main():
    d = {
        'addentity': addEntity,
    }
    r = True
    f = nullfunction
    loadData()
    
    while r:
        cmd = raw_input('> ')
        fnc = d.get(cmd, f)
        fnc()
        if cmd == 'quit':
            r = False
            
        if cmd == 'save':
        

if __name__ == '__main__':
    main()
else:
    warn(Warning('This module is not meant to be imported'))
