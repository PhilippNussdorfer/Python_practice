from actions.Action import Action
from actions.Exit import Exit


class Interpret:

    def __init__(self):
        self.actionList = []
        self.init()

    def init(self):
        exit_action = Exit(["exit", "ex"])
        help_action = Help(["help", "h"])

        self.add_action(exit_action)
        self.add_action(help_action)

    def add_action(self, action):
        self.actionList.append(action)

    def print_commands(self):
        for row in self.actionList:
            print(row.name + " -> ", row.possible_inputs)
        print()

    def interpret(self, usr_input):
        for row in self.actionList:
            for commands in row.possible_inputs:
                if commands == usr_input:
                    row.execute()


class Help(Action):
    def __init__(self, possible_inputs):
        super().__init__()
        self.name = "Help"
        self.possible_inputs = possible_inputs

    def execute(self):
        Interpret().print_commands()
