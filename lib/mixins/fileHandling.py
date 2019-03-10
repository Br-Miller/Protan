"""STUFF

"""


import glob


class freader(): #RECREATE
    """Reading class"""
    def readFile(self, filepath, readtype=str):
        """Reads the file filepath and returns it

        Args:
            filepath: The filepath of the file to be read
            readtype: Object type to be returned (list/str)
        """
        content = None
        with open(filepath) as f:
            if readtype == str : 
                content = f.read()

            elif readtype == list: 
                content = f.readlines()
        return content

    def foldercontents(self, path, ends=True, exten=True, searchfor='*.*'):
        """finds folder contents"""
        files = glob.glob('%s/%s' % (path, searchfor))
        if sys.platform == 'win32':
            s = [''.join(i.split(path.split('/')[-1] + '\\')) for i in files ]

        if ends: 
            files = [ filestr(i).pathend(extension=exten) for i in files ]
            
        return files