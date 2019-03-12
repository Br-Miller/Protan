"""Audio playing class
Plays, contencates, loops and edits audio files
Currently only works on OS
"""


import os
import commands
from subprocess import call


def terminalDoOs(s):
    os.system(s)

def terminalDoSub(l):
    call(['ls', '-l'])

def terminalDoCom(s):
    s=commands.getstatusoutput(s)
    return s


def play(filepath):
    terminalDoSub(['afplay', filepath, '&'])

#afplay filepath &
#killall afplay
