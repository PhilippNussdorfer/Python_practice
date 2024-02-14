import sys
from .Action import Action


class Exit(Action):
    def __init__(self, possible_inputs):
        super().__init__()
        self.name = "Exit"
        self.possible_inputs = possible_inputs

    def execute(self):
        sys.exit()
