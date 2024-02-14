import random


class CreateGameField:
    def __init__(self):
        rows, cols = (3, 3)
        self.game_field = [[" " for i in range(cols)] for j in range(rows)]

    def get_game_field(self):
        return self.game_field


class Players:
    def __init__(self, player0, player1):
        self.player_x = player0
        self.player_o = player1
        self.beginner = random.randint(0, 1)

    def get_starter(self):
        return self.beginner

    def get_player_x(self):
        return self.player_x

    def get_player_o(self):
        return self.player_o


def return_winner(winner, player_x, player_o):
    if winner == "O":
        return player_o
    else:
        return player_x


def handle_win_con(game_field_arr, player_x, player_o):
    for x in range(3):
        if game_field_arr[0][x] != " " and game_field_arr[0][x] == game_field_arr[1][x] and game_field_arr[1][x] == \
                game_field_arr[2][x]:
            return return_winner(game_field_arr[0][x], player_x, player_o)

        if game_field_arr[x][0] != " " and game_field_arr[x][0] == game_field_arr[x][1] and game_field_arr[x][1] == \
                game_field_arr[x][2]:
            return return_winner(game_field_arr[0][x], player_x, player_o)

    if game_field_arr[0][0] != " " and game_field_arr[0][0] == game_field_arr[1][1] and game_field_arr[1][1] == \
            game_field_arr[2][2]:
        return return_winner(game_field_arr[0][0], player_x, player_o)

    if game_field_arr[2][0] != " " and game_field_arr[2][0] == game_field_arr[1][1] and game_field_arr[1][1] == \
            game_field_arr[0][2]:
        return return_winner(game_field_arr[2][0], player_x, player_o)


def print_field(game_field):
    num = 0
    print("    0    1    2")
    for row in game_field:
        print(num, row)
        num += 1


def check_if_free(game_field, coor0, coor1, ):
    if game_field[coor0][coor1] == " ":
        return True
    print("Please enter a valid position.")
    return False


def change_player(player_num):
    if player_num == 0:
        player_num = 1
        return player_num
    else:
        player_num = 0
        return player_num


def get_player_sym(player_num):
    if player_num == 0:
        return "X"
    else:
        return "O"


def get_player(player_num, player_x, player_o):
    if get_player_sym(player_num) == "O":
        return player_o
    return player_x


def game_console(game_field, player_num, player_x, player_o):

    while True:
        if handle_win_con(game_field, player_x, player_o) == player_x:
            return player_x
        elif handle_win_con(game_field, player_x, player_o) == player_o:
            return player_o

        if get_player_sym(player_num) == "O":
            print("It's " + player_o + " turn")
        else:
            print("Its " + player_x + " turn")

        while True:
            print_field(game_field)
            try:
                coor0 = int(input("Please input the row of the fild: "))
                coor1 = int(input("Please Input the colum of the field: "))
                if 3 > coor0 >= 0 and 3 > coor1 >= 0 and check_if_free(game_field, coor0, coor1):
                    game_field[coor0][coor1] = get_player_sym(player_num)
                    break
            except:
                print("Please enter a valid Number")

        player_num = change_player(player_num)


#gameField = CreateGameField()
#gameFieldArr = gameField.get_game_field()
#print("Winner is : " + game_console(gameFieldArr, random.randint(0, 1), "Bob", "Hans"))
