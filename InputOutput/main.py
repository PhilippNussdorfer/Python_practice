"""
Author:      Philipp Nußdorfer
Date:        16.2.2023
Version:     0.1
Description: Is a boring program that asks the user for his or her name and Welcomes the user
             after that it will ask the user for 3 numbers, ads them and gives back an average
"""

user_input = input("Who are you?: ")
print("Welcome ", user_input)
user = user_input

user_input = input("Please enter a number: ")
num1 = int(user_input)
user_input = input("Please enter a number: ")
num2 = int(user_input)
user_input = input("Please enter a number: ")
user_input = int(user_input)

print("{}+{}+{} =".format(num1, num2, user_input), num1 + num2 + user_input)
print("Average of the numbers {}, {}, {} is: ".format(num1, num2, user_input), ((num1 + num2 + user_input) / 2))

print("Goodbye ", user)
