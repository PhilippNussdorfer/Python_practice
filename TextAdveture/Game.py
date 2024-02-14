from Room import Room
from Item import Item
from actions.Interpreter import Interpret


class Game:
    def __init__(self):
        self.active_room = None
        self.create()
        self.interpreter = Interpret()

    def create(self):
        cottage = Room("Cottage", "Its a old cottage in a forest.")
        forest = Room("Forest", "Its an old, dark and scary forest.")
        well = Room("Well", "Its a old well that has still water in it.")

        rope = Item("Rope", "Its a rope.")
        hammer = Item("Hammer", "Its a hammer")
        bucket = Item("Bucket", "Its a Bucket")
        axe = Item("Axe", "Its a old rusty axe")

        cottage.add_item_to_room(axe)
        cottage.add_item_to_room(hammer)
        forest.add_item_to_room(rope)
        well.add_item_to_room(bucket)

        cottage.add_room("s", forest)
        cottage.add_room("n", well)
        forest.add_room("n", cottage)
        well.add_room("s", cottage)

        self.active_room = cottage

    def get_interpreter(self):
        return self.interpreter

    def run_game(self):

        while True:
            self.active_room.print_room_details()
            self.active_room.print_item_details()
            self.active_room.show_directions()

            usr_input = input("\n> ")

            found_room = self.active_room.find_room(usr_input)
            if found_room is not None:
                self.active_room = found_room

            self.interpreter.interpret(usr_input)
