import random
import os.path

"""
    Author:      Philipp Nußdorfer
    Date:        16.2.2023
    Version:     0.1.8
    Description:
"""

LIVES = 3
APPLE_LIVES = 15
SCORE = 0
APPLE = ""
ORIENTATION = ["A", "<", "v", ">"]
SNAKE = [ORIENTATION[2]]
SNAKE_HEAD_POS = ""
SNAKE_BODY_POS = []
WIN = False

"""
    Adds a body segment on the position where the head was
    should be done before the head gets the new cords
"""


def add_body_to_snake(game_field_arr):
    global SNAKE
    global SNAKE_HEAD_POS
    pos = SNAKE_HEAD_POS.split(";")
    SNAKE.insert(0, "#")
    SNAKE_BODY_POS.insert(0, SNAKE_HEAD_POS)
    game_field_arr[int(pos[0])][int(pos[1])] = SNAKE[0]
    return game_field_arr


"""
    returns the Snake head
"""


def get_snake_head():
    return SNAKE[len(SNAKE) - 1]


"""
    sets the orientation in witch the the snake is looking
"""


def set_snake_orientation(orientation_int):
    global SNAKE
    SNAKE[len(SNAKE) - 1] = ORIENTATION[orientation_int]


"""
    returns True or False if the Apple cords are set or not
"""


def has_apple_cords(apple):
    if apple != "":
        return True
    return False


"""
    Sets the new cords of the apple
"""


def set_new_apple_cords():
    global APPLE
    APPLE = str(random.randint(0, 7)) + ";" + str(random.randint(0, 7))


"""
    Sets the new cords of the snake head
"""


def set_snake_head_cords(cor_y, cor_x):
    global SNAKE_HEAD_POS
    SNAKE_HEAD_POS = str(cor_y) + ";" + str(cor_x)


"""
    first it deletes the entire body from the snake in the game field 
    then it will set the position of the body parts the last part gets the cords of part before until it reaches the 
    first body part that gets the position of the head
    and lastly the snake body will be set with the new coordinates in the game field
    
    needs an array of the game field
    
    returns the game field where the snake body is is on its new positions
"""


def set_snake_body_on_move(game_field_arr):
    global SNAKE_BODY_POS
    for i in range(len(SNAKE_BODY_POS)):
        pos = SNAKE_BODY_POS[i].split(";")
        game_field_arr[int(pos[0])][int(pos[1])] = " "
    for i in range(len(SNAKE) - 2, 0, -1):
        if i > 0:
            SNAKE_BODY_POS[i] = SNAKE_BODY_POS[i - 1]
    SNAKE_BODY_POS[0] = SNAKE_HEAD_POS

    for i in range(len(SNAKE_BODY_POS)):
        pos = SNAKE_BODY_POS[i].split(";")
        game_field_arr[int(pos[0])][int(pos[1])] = SNAKE[i]
    return game_field_arr


"""
    Tests if the player has won the game or not
"""


def test_for_winn(game_field_arr):
    global SCORE
    global WIN
    if any(" " in sublist for sublist in game_field_arr) or any("O" in sublist for sublist in game_field_arr):
        WIN = False
    else:
        WIN = True
        SCORE += 50


"""
    deletes the old position of the apple, adds a score point and will reset the Apple lives.
"""


def apple_eaten():
    global APPLE
    global SCORE
    global APPLE_LIVES
    APPLE = ""
    SCORE += 1
    APPLE_LIVES = 15


"""
    subtracts a live point
"""


def snake_losses_life():
    global LIVES
    LIVES -= 1


"""
    sets the apple in the game field on a random position runs as long until it finds a free space in the
    
    returns the game field with the Apple
"""


def place_apple_in_game_field(game_field_arr):
    if has_apple_cords(APPLE):
        while True:
            if WIN:
                break
            pos = APPLE.split(";")
            if game_field_arr[int(pos[0])][int(pos[1])] != " ":
                set_new_apple_cords()
            else:
                game_field_arr[int(pos[0])][int(pos[1])] = "O"
                break

    else:
        set_new_apple_cords()
        while True:
            if WIN:
                break
            pos = APPLE.split(";")
            if game_field_arr[int(pos[0])][int(pos[1])] != " ":
                set_new_apple_cords()
            else:
                game_field_arr[int(pos[0])][int(pos[1])] = "O"
                break
    return game_field_arr


"""
    get_game_field()
    creates a 2D array that is used as the game field and
    sets the start point of the snake
    
    returns the Beginning Array of the game field
"""


def get_game_field():
    game_field_arr = [[" " for i in range(8)] for j in range(8)]
    place_apple_in_game_field(game_field_arr)
    global SNAKE

    if game_field_arr[0][0] != "O":
        game_field_arr[0][0] = SNAKE[len(SNAKE) - 1]
        set_snake_head_cords(0, 0)
    else:
        game_field_arr[0][1] = SNAKE[len(SNAKE) - 1]
        set_snake_head_cords(0, 1)
    return game_field_arr


"""
    handles the snake movement
    if the snake hits a wall or everything else other than " " or "O" the snake will lose e life
    else the snake moves normal until it eats an apple then the snake head will move up and a new segment of the snake 
    will appear where the head was before
    
    needs pos0 and pos1, they ar the integer where the head moves, a array of the game field and the int for the
    orientation of the head
    
    returns a array of the game field or None if the snake hits the wall or bites its self
"""


def move_snake(pos0, pos1, game_field_arr, orientation_int):
    global SNAKE_HEAD_POS
    global APPLE_LIVES
    APPLE_LIVES -= 1
    has_eaten = False
    pos = SNAKE_HEAD_POS.split(";")
    if ((0 <= pos0 <= 7) and (0 <= pos1 <= 7)) and \
            (game_field_arr[pos0][pos1] == " " or game_field_arr[pos0][pos1] == "O"):

        set_snake_orientation(orientation_int)

        if game_field_arr[pos0][pos1] == "O":
            apple_eaten()
            game_field_arr = add_body_to_snake(game_field_arr)
            game_field_arr = place_apple_in_game_field(game_field_arr)
            has_eaten = True

        if not SNAKE_BODY_POS:
            game_field_arr[int(pos[0])][int(pos[1])] = " "
        elif not has_eaten:
            game_field_arr = set_snake_body_on_move(game_field_arr)
        SNAKE_HEAD_POS = str(pos0) + ";" + str(pos1)

        game_field_arr[pos0][pos1] = get_snake_head()
        return game_field_arr
    else:
        snake_losses_life()


"""
    handles the return value of move_snake() 
    if the return value is None it will return the old game field
    else it returns the new game field
    
    needs an int for the movement, a game field(array), a int for the orientation of the snake and 
    if the snake moves up , down or let , right (True for up and down False for left and right)
    
    gives back a array of th game field
"""


def move_if_not_none(move_int, game_field_arr, orientation_int, up_or_down):
    pos = SNAKE_HEAD_POS.split(";")
    if up_or_down:
        game_field_arr_new = move_snake(int(pos[0]) + move_int, int(pos[1]), game_field_arr, orientation_int)
    else:
        game_field_arr_new = move_snake(int(pos[0]), int(pos[1]) + move_int, game_field_arr, orientation_int)
    if game_field_arr_new is not None:
        return game_field_arr_new
    return game_field_arr


"""
    distributes the user inputs 
    for: 'W' - up, 's' - down,
         'a' - left. 'd' - right
         
    needs a user input and a array of the game field
    
    returns an array of the game field
"""


def move_input_distributor(user_input, game_field_arr):
    global SNAKE
    if user_input.lower() == "w":
        return move_if_not_none(-1, game_field_arr, 0, True)

    elif user_input.lower() == "a":
        return move_if_not_none(-1, game_field_arr, 1, False)

    elif user_input.lower() == "s":
        return move_if_not_none(1, game_field_arr, 2, True)

    elif user_input.lower() == "d":
        return move_if_not_none(1, game_field_arr, 3, False)

    else:
        print("Please enter a valid input.")
    return game_field_arr


"""
    prints the game field and needs an array
"""


def print_game_field(game_field_arr):
    print("\n\nLives: {}  - AppleLives: {}  - Score: {}".format(LIVES, APPLE_LIVES, SCORE))
    ASCII = 65
    print("-" * 30)

    for i in game_field_arr:
        print(chr(ASCII), end=" |  ")
        for j in i:
            print(j, end="  ")
        ASCII += 1
        print("|")

    print("-" * 30)
    print("    ", end="")
    for i in range(len(game_field_arr)):
        print(i, end="  ")


"""
    gives back the second list value as int for the sort
"""


def sort_after(list_row):
    return int(list_row[1])


"""
    Prints the scoreboard if the player wants to see it
    reverses the sort so the top player is on top
"""


def print_scoreboard():
    sort_list = []
    with open("Scores.txt", "r") as all_scores:
        for line in all_scores:
            line = line.strip()
            sort_list.append(line.split(";"))
    sort_list.sort(key=sort_after, reverse=True)
    for string in sort_list:
        print("{} - Score: {} - Lives: {} - Snake Length: {}".format(string[0], string[1], string[2], string[3]))


"""
    
"""


def head_start(game_field_arr):
    while SCORE < 10:

        ap_cor0 = int(APPLE.split(";")[0])
        ap_cor1 = int(APPLE.split(";")[1])
        sn_cor0 = int(SNAKE_HEAD_POS.split(";")[0])
        sn_cor1 = int(SNAKE_HEAD_POS.split(";")[1])

        print_game_field(game_field_arr)

        if ap_cor0 != sn_cor0 and sn_cor0 < ap_cor0 and (game_field_arr[sn_cor0 + 1][sn_cor1] == " " or game_field_arr[sn_cor0 + 1][sn_cor1] == "O"):
            game_field_arr = move_snake(sn_cor0 + 1, sn_cor1, game_field_arr, 2)
        elif ap_cor0 != sn_cor0 and sn_cor0 > ap_cor0 and (game_field_arr[sn_cor0 - 1][sn_cor1] == " " or game_field_arr[sn_cor0 - 1][sn_cor1] == "O"):
            game_field_arr = move_snake(sn_cor0 - 1, sn_cor1, game_field_arr, 0)

        elif ap_cor1 != sn_cor1 and sn_cor1 > ap_cor1 and (game_field_arr[sn_cor0][sn_cor1 - 1] == " " or game_field_arr[sn_cor0][sn_cor1 - 1] == "O"):
            game_field_arr = move_snake(sn_cor0, sn_cor1 - 1, game_field_arr, 1)
        elif ap_cor1 != sn_cor1 and sn_cor1 < ap_cor1 and (game_field_arr[sn_cor0][sn_cor1 + 1] == " " or game_field_arr[sn_cor0][sn_cor1 + 1] == "O"):
            game_field_arr = move_snake(sn_cor0, sn_cor1 + 1, game_field_arr, 3)

        elif sn_cor0 - 1 >= 0 and (game_field_arr[sn_cor0 - 1][sn_cor1] == " " or game_field_arr[sn_cor0 - 1][sn_cor1] == "O"):
            game_field_arr = move_snake(sn_cor0 - 1, sn_cor1, game_field_arr, 0)
        elif sn_cor0 + 1 <= 7 and (game_field_arr[sn_cor0 + 1][sn_cor1] == " " or game_field_arr[sn_cor0 + 1][sn_cor1] == "O"):
            game_field_arr = move_snake(sn_cor0 + 1, sn_cor1, game_field_arr, 2)

        elif sn_cor1 - 1 >= 0 and (game_field_arr[sn_cor0][sn_cor1 - 1] == " " or game_field_arr[sn_cor0][sn_cor1 - 1] == "O"):
            game_field_arr = move_snake(sn_cor0, sn_cor1 - 1, game_field_arr, 1)
        elif sn_cor1 + 1 <= 7 and (game_field_arr[sn_cor0][sn_cor1 + 1] == " " or game_field_arr[sn_cor0][sn_cor1 + 1] == "O"):
            game_field_arr = move_snake(sn_cor0, sn_cor1 + 1, game_field_arr, 3)
        else:
            global LIVES
            LIVES = LIVES - 1

        if LIVES == 0:
            break
    return game_field_arr


"""
    Runs the game until the player loses or he/she decides to exit the program
    asks for inputs from the player for where to move (w,a,s,d) or exit and scoreboard
"""
fails = 0

for i in range(1000):
    game_field = get_game_field()
    game_field = head_start(game_field)
    if LIVES == 0:
        fails = fails + 1
    print_game_field(game_field)
    SCORE = 0
    SNAKE_BODY_POS = []
    LIVES = 3
    APPLE_LIVES = 15
    SNAKE = ["v"]

print("\n\n>> " + str(fails))

"""
def run_game():
    global APPLE_LIVES
    global LIVES
    game_field = get_game_field()

    option = input("0 -> Normal\n1 -> Head start\n> ")
    if option == "1":
        game_field = head_start(game_field)

    while True:
        print_game_field(game_field)
        test_for_winn(game_field)
        if WIN:
            print("\nYou have won the game your score is: ", SCORE)
            break

        player_input = input(
            "\n\ninput [w a s d] or exit to stop the program or enter scoreboard to see all the scores\n> ")
        if player_input == "exit":
            print("\nGoodbye and have a nice day, your score is: ", SCORE)
            break

        if player_input == "scoreboard":
            print_scoreboard()

        if APPLE_LIVES == 0:
            LIVES -= 1
            APPLE_LIVES = 15

        if player_input != "scoreboard":
            game_field = move_input_distributor(player_input, game_field)

        if LIVES == 0:
            print("\nYou have lost, your score is: ", SCORE)
            break


player = input("Pleas enter your player name\n> ")
if not player:
    player = "no_name"
run_game()
if not os.path.isfile("Scores.txt"):
    file_create = open("Scores.txt", "x")
    print("created file")

file_write = open("Scores.txt", "a")
file_write.write("{};{};{};{}\n".format(player, SCORE, LIVES, len(SNAKE_BODY_POS)))
file_write.close()
"""
