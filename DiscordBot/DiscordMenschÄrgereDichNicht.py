import math
import random


def get_multiplier(count_of_players):
    multiplier = count_of_players - 4
    return math.ceil(multiplier / 2)


def dice():
    return random.randint(1, 6)


"""
create_ludo_game_field()
creates a game field for the game ludo (Mensch ärgere dich nicht (in german))
will create a game field based on the count of players if the count of players
"""


def create_ludo_game_field(count_of_players):
    game_field = 0
    if count_of_players < 5:
        game_field = [[" " for i in range(13)] for j in range(13)]
    elif count_of_players > 4:
        game_field = [[" " for i in range(13 + (6 * get_multiplier(count_of_players)))] for j in
                      range(13 + (6 * get_multiplier(count_of_players)))]

    for i in range(len(game_field)):
        for j in range(len(game_field)):
            if i == 0 or i == len(game_field) - 1:
                game_field[i][j] = "X"
            elif j == 0 or j == len(game_field) - 1:
                game_field[i][j] = "X"

    return game_field


def get_count_of_players(players_arr):
    return len(players_arr)


def check_win(game_field, player_pins):
    return None


def print_game_field(game_field_arr):
    for row in game_field_arr:
        print(row)


print_game_field(create_ludo_game_field(7))
