"""
Challenge:
Using the Python language, have the function QuestionsMarks(str) take the str 
string parameter, which will contain single digit numbers, letters, and question 
marks, and check if there are exactly 3 question marks between every pair of two 
numbers that add up to 10. If so, then your program should return the string true, 
otherwise it should return the string false. If there aren't any two numbers that 
add up to 10 in the string, then your program should return false as well. 

For example: if str is "arrb6???4xxbl5???eee5" then your program should return True 
because there are exactly 3 question marks between 6 and 4, and 3 question marks between 
5 and 5 at the end of the string.

Sample Test Cases
Input:"aa6?9"
Output:"false"
Input:"acc?7??sss?3rr1??????5"
Output:"true"
"""


from string import digits
    

def QuestionsMarks(s, intSum=10, sep='?', sepNo=3): #Very Slightly More Efficient Design
  """Whether there are exactly sepNo characters sep between every pair of two numbers that add up to intSum"""
  assert isinstance(s, str), "incorrect type of arg s: should be type str, is type {}".format(type(s))
  assert isinstance(intSum, int), "incorrect type of arg intSum: should be type int, is type {}".format(type(intSum))
  assert isinstance(sep, str), "incorrect type of arg sep: should be type str, is type {}".format(type(sep))
  assert isinstance(sepNo, int), "incorrect type of arg sepNo: should be type int, is type {}".format(type(sepNo))

  digitArray = []
  indexArray = []

  for index, character in enumerate(s): #If the character is a digit, add the index and digit to the correct array
    if character in digits:
      digitArray.append(int(character))
      indexArray.append(index)
  
  for i, x in enumerate(digitArray[:-1]): #Create a new array with the middle of matching pairs
    if x + digitArray[i + 1] == intSum:
      if s[indexArray[i]: indexArray[i + 1]].count(sep) != sepNo:
        return False

  return True


def QuestionsMarksR(s, intSum=10, sep='?', sepNo=3): #More Readable Design
  """Whether there are exactly sepNo characters sep between every pair of two numbers that add up to intSum"""
  assert isinstance(s, str), "incorrect type of arg s: should be type str, is type {}".format(type(s))
  assert isinstance(intSum, int), "incorrect type of arg intSum: should be type int, is type {}".format(type(intSum))
  assert isinstance(sep, str), "incorrect type of arg sep: should be type str, is type {}".format(type(sep))
  assert isinstance(sepNo, int), "incorrect type of arg sepNo: should be type int, is type {}".format(type(sepNo))

  digitArray = []
  indexArray = []

  for index, character in enumerate(s): # If the character is a digit, add the index and digit to the correct array
    if character in digits:
      digitArray.append(int(character))
      indexArray.append(index)
  
  stringArray = []
  for i, x in enumerate(digitArray[:-1]): #Create a new array with the indexes
    if x + digitArray[i + 1] == intSum:
      stringArray.append(indexArray[i: i+2])

  stringArray = map(lambda x: s[x[0]: x[1]], stringArray) #Get the middle of the indexes
  stringArray = map(lambda x: x.count(sep), stringArray) #Count seperators
  stringArray = map(lambda x: x == sepNo, stringArray) #Check if seperators equals sepNo

  return sum(stringArray) == len(stringArray) and len(stringArray) != 0