# Author: Philipp Nussdorfer
# Date: 22.9.2022
# version: 0.1

# Description: is a calculator for grades

points = 0
grade = ""
end = False     # so long as it is false teh program will not stop

while True:     # a while loop that runs so long until it's stopped with break

    while True:     # this while runs so long until the user can input a valid
        i = input("Enter your archived points for the challenge: ")
        if i.isnumeric():       # asks input if it is numeric
            integer = int(i)        # casts the String of input into an integer
            if 0 <= integer <= 20:      # asks integer if the input is 0 or between 0 and 20 0r is 20
                points += integer       # adds the number of the input to the points
                break       # stops the while loop
            else:
                print("Input Error. Please enter an valid integer between 0 and 20!")
        else:
            print("Input Error. Please enter an valid integer between 0 and 20!")

    while True:     # this while runs so long until the user can input a valid
        i = input("Enter your archived points for the exam: ")
        if i.isnumeric():       # asks input if it is numeric
            integer = int(i)        # casts the String of input into an integer
            if 0 <= integer <= 70:      # asks integer if the input is 0 or between 0 and 70 0r is 70
                points += integer       # adds the number of the input to the points
                break       # stops the while loop
            else:
                print("Input Error. Please enter an valid integer between 0 and 70!")
        else:
            print("Input Error. Please enter an valid integer between 0 and 70!")

    while True:     # this while runs so long until the user can input a valid
        i = input("Did you attend the vocal presentation? ")
        if i == "yes":
            while True:     # this while runs so long until the user can input a valid
                i = input("Enter the achieved points for the vocal presentation: ")
                if i.isnumeric():       # asks input if it is numeric
                    integer = int(i)        # casts the String of input into an integer
                    if integer == 0:        # asks the integer if the input is the same as 0
                        print("You need more than 0 points on the vocal presentation to pass this course.")
                        points -= 50        # removes 50 points if the user types in 0
                        end = True      # with end will end the program and will give you your grade
                        break       # stops the while loop
                    elif 0 < integer <= 10:     # asks integer if the input is between 0 and 10 0r is 10
                        points += integer       # adds the number of the input to the points
                        print("Out of 100 possible points you scored: {}".format(points))       # with format will be the points where the {} ar
                        end = True      # with end will end the program and will give you your grade
                        break       # stops the while loop
                    else:
                        print("Input Error. Please enter an valid integer between 0 and 10!")
                else:
                    print("Input Error. Please enter an valid integer between 0 and 10!")
        if end:     # needs end to be True to stop the whileloop
            break       # stops the while loop
        elif i == "no":     # if the user decided to say NO then the program will answer with it is mandatory
            print("The vocal presentation is mandatory!")
        else:
            print("Input Error. Please enter either 'yes' or 'no'.")

    if end:     # if end is True you get your grade

        if points < 0:  # if points go under 0 so this is for preventing an error
            points = 0

        if points >= 90:
            grade = "A (1)"     # I used the UK Grade letters
            break       # stops the while loop

        elif points >= 80:
            grade = "B (2)"
            break       # stops the while loop

        elif points >= 65:
            grade = "C (3)"
            break       # stops the while loop

        elif points >= 50:
            grade = "D (4)"
            break       # stops the while loop

        elif points >= 0:
            grade = "E (5)"
            break       # stops the while loop


print("Based on your input your grade will be: " + grade)       # Output of your grade :D
