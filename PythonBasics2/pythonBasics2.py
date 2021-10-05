# Python Activity
#
# Fill in the code for the functions below.
# The starter code for each function includes a 'return'
# which is just a placeholder for your code. Make sure to add what is going to be returned.


# Part A. count_threes
# Define a function count_threes(n) that takes an int and
# returns the number of multiples of 3 in the range from 0
# to n (including n).

def count_threes(n):

  n = list(str(n))

  diction = {}

  diction[3] = diction[6] = diction[9] = 0

  for i in n:
      j = int(i)
      if j % 3 == 0 and j != 0:
          diction[j] = diction[j] + 1

  max = -1
  indx = -1

  for k, v in diction.items():
      if v > max:
          max = v
          indx = k

  return indx

# Part B. longest_consecutive_repeating_char
# Define a function longest_consecutive_repeating_char(s) that takes
# a string s and returns the character that has the longest consecutive repeat.
def longest_consecutive_repeating_char(s):


  s = list(s)
  l = len(s)
  count = 1

  diction = {}

  for i in range(0, l - 1):
      if (s[i] != s[i + 1]):
          if ((s[i] in diction) and diction[s[i]] > count):
              continue
          else:
              diction[s[i]] = count
              count = 1
      else:
          count += 1

  diction[s[l - 1]] = count

  max = -1
  for key, value in diction.items():
      if value > max:
          max = value

  lst = []
  for key, value in diction.items():
      if value == max:
          lst.append(key)

  return lst




# Part C. is_palindrome
# Define a function is_palindrome(s) that takes a string s
# and returns whether or not that string is a palindrome.
# A palindrome is a string that reads the same backwards and
# forwards. Treat capital letters the same as lowercase ones
# and ignore spaces (i.e. case insensitive).
def is_palindrome(s):
    i = 0
    j = len(s)-1
    while i <= j:
        if s[i] == ' ':
            i += 1
            continue
        if s[j] == ' ':
            j -= 1
            continue
        if s[i].lower() != s[j].lower():
            return False
        i += 1
        j -= 1
    return True

