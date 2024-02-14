from calculator.add import Add
from calculator.subtract import Subtract


class Iterpreter:

    def interpret(self, operation, num, sec_num):
        operations = [Add('+'), Subtract('-')]
        for x in operations:
            if x.operator == operation:
                return x.calc(num, sec_num)
