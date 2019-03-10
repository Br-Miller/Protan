"""
Profanity Filter
"""


import re


regexBackslash = ['\\', '(', ')', '[', '|', '.', '+', '^', '*']
wildcards = ['\\*', '\\^', '-', '\\.']
goodwords = [

]
badwords = [
  ' fuk',
  ' fuc',
  'fuck',
  'fucker',
  'fucking',
  'bitch',
  'cunt',
  'bastard',
  ' ass',
  'whore',
  'shit',
  'penis',
  'dick',
  'cock',
  'vagina',
]
slurs = {
  'a': ['a', '4', '@', '^'],
  'b': ['b', '*', '13', 'lo', 'j3', '|3', '|}', '|:', '|8', '18', '6', '|b', '|o'],
  'c': ['c', '<', '{', '[', '('],
  'd': ['d', '|)', '|}', '|]', '|>'],
  'e': ['e', '3'],
  'f': ['f', '|=', 'ph', '|#', '|"'],
  'g': ['g' '[', '+', '[+', '6', 'c-'],
  'h': ['h', '4', '|-|', '[-]', '{-}', '}-{', '}{', '|=|', '[-]', '/-/', '(-)', ')-(', ':-:', 'i+i', '#'],
  'i': ['i', '1', '|', '!', '9'],
  'j': ['j', '_|', '_/', '_7', '_)', '_]', '_}'],
  'k': ['k', '|<', '1<', 'l<', '|{', 'l{'],
  'l': ['l', '|_', '|', '1', ']['],
  'm': ['m', '44', '|\\/|', '^^', '/\\/\\', '/x\\', '[]v[]', '][\\\\//][', '(V)', '//\\\\//\\\\', 'n\\'],
  'n': ['n', '|\\|', '/\\/', '/V', '][\\\\]['],
  'o': ['o', '0','()', '[]', '{}', '<>', 'oh'],
  'p': ['p', '|o', '|O', '|>', '|*', '|D', '/o', '[]D', '|7'],
  'q': ['q', 'O_', '9', '(,)', '0', 'kw'],
  'r': ['r', '|2', '12', '.-', '|^', 'l2'],
  's': ['s', '5', '\$'],
  't': ['t', "7", "+", "7`", "'|'" , "`|`" , "~|~" , "-|-", "']['"],
  'u': ['u', '|_|','\\_\\', '/_/', '\\_/', '(_)', '[_]', '{_}', 'v', '\\/'],
  'v': ['v', '\\/', 'u'],
  'w': ['w', '\\/\\/', '(/\\)', '\\^/', '|/\\|', '\\X/', '\\\\\'', '\'//', 'VV', '\\_|_/', '\\\\//\\\\//', '2u', '\\V/'],
  'x': ['x', '%', '*', '><', '}{', ')('],
  'y': ['y', '`/', '\\|/', '4'],
  'z': ['z', '2', '5', '7_', '>_,(/)'],
}

def convertSlurs():
  for element in slurs.keys():
    l = slurs[element]
    newa = [ i for i in wildcards ]
    for i in l:
      for j in regexBackslash:
        i = i.replace(j, '\\' + j)
      newa.append(i)
    s = '(' + '|'.join(newa) + ')'
    slurs[element] = s

def convertBadWords():
  global badwords
  badwords = [ (i, re.compile(''.join([ slurs.get(c, '({})'.format(c)) for c in i ]))) for i in badwords ]

def main():
  convertSlurs()
  convertBadWords()

def isprofane(s):
  s = s.lower()
  for k, v in badwords:
    if re.findall(v, s):
      return True
  return False

main()
