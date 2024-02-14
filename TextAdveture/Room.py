class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = []
        self.items_in_room = []

    def add_room(self, direction, room):
        self.exits.append((direction, room))

    def print_room_details(self):
        print("You are here:")
        print(self.name + "\n" + self.description + "\n")

    def show_directions(self):
        print("Those are the directions that you can go:")
        for row in self.exits:
            print(row[0])

    def print_item_details(self):
        print("Those are the items in the vicinity:")
        for row in self.items_in_room:
            print(row.name + " -> " + row.description)
        print()

    def find_room(self, usr_input):
        for row in self.exits:
            if row[0] == usr_input:
                return row[1]
        return None

    def add_item_to_room(self, item):
        self.items_in_room.append(item)
