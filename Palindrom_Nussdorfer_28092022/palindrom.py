# Author: Philipp Nussdorfer
# Version: 0.1
# Date: 28.9.2022

# Description: Sagt dir ob eine oder alle der zahlen die man eingegeben hat ein palindrom sind oder nicht

def main():
    my_input_number = 0
    my_inputs = []

    for x in range(5):  # fragt dich fünf mal um eine zahl die in eine liste gespeichert werden
        user_input = input("Bitte geben sie eine zahl ein: ")
        if user_input.isnumeric():  # fragt ob der string eine zahl ist und wenn ja wird sie als zahl gespeichert und dann in die liste gepackt falls der input nicht numeric ist wird statdessen eine null gespeichert
            my_input_number = int(user_input)
        my_inputs.append(my_input_number)  # dies ist die liste wo die zahlen hineingespeichert werden

    return my_inputs  # gibt die liste für weitere verwendung zurück


def palindrome():
    my_palindrome_list = main()  # speichert die liste von main in my_palindrome_list
    my_reversed_input = []  # die umgedrehten zahlen werden in diese liste gespeichert

    for i in range(
            5):  # wiederholt die schleife 5 mal und speichert in jeden durchlauf jeweils 0,1,2,3,4 in i pro durchlauf also im ersten durchlauf i = 0 im zweiten i = 1 usw.
        my_number = my_palindrome_list[i]
        number = 0

        while my_number != 0:  # wiederholt sich solange my_number nicht gleich null ist
            digit = my_number % 10  # digit ist der rest der dann weiterverwendet wird
            number = number * 10 + digit  # number wird  mal 10 gerechnet und dan die digit hinzugefügt bis die es durch die ganze zahl ist und die schleife abgebrochen wird
            my_number //= 10  # damit die schleife nicht andauernt 121 oder was auch immer die zahl die verwendet wird ist und damit weiter leuft und das programm auch hier abbricht

        my_reversed_input.append(number)  # hier werden die zahlen ind die liste gespeichert

    for i in range(5):

        if my_palindrome_list[i] == my_reversed_input[i]:  # für den output
            print("{} ist ein Palindrom".format(my_palindrome_list[i]))
        else:
            print("{} ist kein Palindrom".format(my_palindrome_list[i]))


palindrome()  # startet das ganze
