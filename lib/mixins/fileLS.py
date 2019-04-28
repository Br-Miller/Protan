"""File related functions

"""


import os
import sys
import glob
import json
import pickle
import marshal


class FStr():
    """Filepath editingclass"""
    @staticmethod
    def join(l):
        """Joins a list of directories"""
        os.path.sep.join(l)

    @staticmethod
    def split(s):
        """Splits a filepath"""
        return s.split(os.path.sep)

    @staticmethod
    def ftype(s):
        """Returns the file extension of a file, file if none"""
        s = FStr.split(s)
        if '.' not in s:
            return 'file'
        return s.split('.')[1]

    @staticmethod
    def name(s):
        """Returns the name of a file"""
        s = FStr.split(s)[-1]
        s = s.split('.')[0]
        return s

class FileLS():
    """File loading and deserialising class"""
    serialiseDict = {
        None: lambda s: s,
        'json': json.dumps,
        'pickle': pickle.dumps,
        'marshal': marshal.dumps,
        'j': json.dumps,
        'p': pickle.dumps,
        'm': marshal.dumps
    }
    deserialiseDict = {
        None: lambda s: s,
        'json': json.loads,
        'pickle': pickle.loads,
        'marshal': marshal.loads,
        'j': json.dumps,
        'p': pickle.dumps,
        'm': marshal.dumps
    }
    @staticmethod
    def serialise(s, tpe=None):
        func = FRead.serialiseDict[tpe]
        return func(s)

    @staticmethod
    def deserialise(s, tpe=None):
        assert isinstance(s, str), 'incorrect type of arg s: should be type str, is type {}'.format(type(s))
        func = FRead.deserialiseDict[tpe]
        return func(s)
        return s

    @staticmethod
    def _write(path, s, tpe='r'):
        try:
            f = open(path, tpe)
            f.write(s)
            f.close()
        except Exception:
            pass

    @staticmethod
    def _read(path):
        try:
            f = open(path)
            content = f.read()
            f.close()
            return content
        except IOError:
            return IOError('Could not find file')

    @staticmethod
    def write(path, data, s=None):
        """Serialises data then writes it to a file
        Serialises file contents

        Args:
            s: Serialisation type
            path: The path of the file to be written to
        """
        data = FRead.serialise(data, tpe=s)
        FRead._write(path, data)

    @staticmethod
    def read(path, s=None, d=None, w=None):
        """Reads a file and deserialises the result
        Deserialises file contents or rewrites them on error

        Args:
            s: Serialisation type type
            d: Returns d on error, if not, returns an error
            w: Should write to file if not found?
            path: The path of the file to be read
        """
        f = FRead._read(path)
        f = FRead.readE(path, f, s=s, d=d, w=w)
        f = FRead.deserialise(f, tpe=s)
        return f

    @staticmethod
    def readE(path, contents, ser=None, default=None, write=None):
        """Ensures that there isn't a error."""
        if isinstance(f, IOError):
            contents = default or contents

            if write and d:
                FRead.write(path, default, ser=ser)
        return contents


class FGlob():
    """File sifting and checking class"""
    @staticmethod
    def globf(path, ends=True, exten=True, searchfor='*.*'):
        """finds folder contents"""
        files = glob.glob('%s/%s' % (path, searchfor))
        if sys.platform == 'win32':
            s = [''.join(i.split(path.split('/')[-1] + '\\')) for i in files ]

        if ends: 
            files = [ filestr(i).pathend(extension=exten) for i in files ]
            
        return files
        
