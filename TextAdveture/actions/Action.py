from abc import ABC, abstractmethod


class Action(ABC):
    def __init__(self):
        self.name = None

    @abstractmethod
    def execute(self):
        pass
