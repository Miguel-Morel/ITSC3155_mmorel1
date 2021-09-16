# Python Activity
#
# Fill in the code for the functions below.
# The starter code for each function includes a 'return'
# which is just a placeholder for your code. Make sure to add what is going to be returned.

# Part A. odd_range
# Define a function odd_range(num1, num2) that takes a starting number (num1) and an ending number (num2)
# and returns all odd numbers as an array between num1 (inclusive) and num2 (exclusive)
def odd_range(num1, num2):
  array = []

  for i in range(num1, num2):
    if i % 2 != 0:
      array.append(i)
  return array



# Part B. has_lower_case
# Define a function has_lower_case(s) that takes a string s
# and checks if string s contains a lower case char.
# The function should return True indicating that string s has a lower case char
# otherwise return False
def has_lower_case(s):
  for sx in s:
    if sx.islower():
      return True

  return False


# Part C. fizz_buzz
# Define a function fizz_buzz(num) that takes an integer num
# and returns a string based on the following criteria:

# if num is divisible by 3 return "Fizz"
# if num is divisible by 5 return "Buzz"
# if num is divisible by 3 and 5 return "FizzBuzz"

# if num is does not meet any of the above criteria or is less than
# or equal to 0 return the num as a string
def fizz_buzz(num):
  if num < 0:
    return str(num)
  elif num == 0:
    return str(num)
  elif (num % 3) == 0 and (num % 5) == 0:
    return "FizzBuzz"
  elif (num % 5) == 0:
    return "Buzz"
  elif (num % 3) == 0:
    return "Fizz"
  return str(num)
