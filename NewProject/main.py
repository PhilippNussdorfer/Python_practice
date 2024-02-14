import math

import switch as switch


def add(x, y):
    print(x + y)


def div(x, y):
    if x == 0:
        print(0)
    else:
        print(x / y)


def multi(x, y):
    print(x * y)


def sub(x, y):
    print(x - y)


def sqrt(x):
    print(math.sqrt(x))


def potenz(x, y):
    print(pow(x, y))


def min(x, y):
    print(min(x, y))


def max(x, y):
    print(max(x, y))


def absoluterWert(x, y):
    a = {abs(x), abs(y)}
    print(a)


def durchschnitt(x, y):
    print(x+y/2)


loop = True
while loop:

    end = input("Exit?: ")
    if end == "yes":
        loop = False
    x = input("Erste zahl: ")
    y = input("Zweite zahl: ")
    try:
        x = float(x)
        y = float(y)
    except:
        print("is not possible")

    opera = input("mit welchen operator wollen sie rechnen: ")


def operatoren(operator):
    switch = {
        '+': add(x, y),
        '-': sub(x, y),
        '/': div(x, y),
        '*': multi(x, y),
        'p': potenz(x, y),
        's': sqrt(x),
        'd': durchschnitt(x, y),
        'a': absoluterWert(x, y),
        'min': min(x, y),
        'max': max(x, y)
    }
    return switch.get(operator, "invalid input")

def oper(operator):
    try:
        match operator:
            case "+":
                add(x, y)
            case "-":
                sub(x, y)
            case "*":
                multi(x, y)
            case "/":
                div(x, y)
    except:
        print("ist nicht moiglich")



oper(opera)
