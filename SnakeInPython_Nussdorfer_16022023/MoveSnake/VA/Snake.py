import numpy
import random


class Snake:
    def __init__(self, game_field_size):
        self.lives = 3
        self.orientation = ['^', '>', 'v', '<']
        self.snake = [self.orientation[2]]
        self.snakePos = [[0, 0]]
        self.head_color = (15, 137, 35)
        self.body_color = (50, 255, 81)
        self.game_field_size = game_field_size
        self.gameFieldArr = None
        self.eaten = False
        self.lost_live = False
        self.moves = (game_field_size * 2) - 1
        self.reset_moves = (game_field_size * 2) - 1

    def create_game_field(self):
        self.gameFieldArr = numpy.full((self.game_field_size, self.game_field_size), " ")

    def reset_snake(self):
        self.snake = [self.orientation[2]]
        self.snakePos = [[0, 0]]

    def add_body(self, pos0, pos1):

        self.snake.insert(0, '#')
        self.snakePos.insert(0, [pos0, pos1])

    def move_dire(self, up_down, move_int):
        head_pos = len(self.snake) - 1
        pos0 = self.snakePos[head_pos][0]
        pos1 = self.snakePos[head_pos][1]

        if up_down and (0 <= (pos0 + move_int) <= len(self.gameFieldArr) - 1) and \
                (self.gameFieldArr[pos0 + move_int][pos1] == " " or self.gameFieldArr[pos0 + move_int][pos1] == "O"):
            pos = [self.snakePos[head_pos][0] + move_int, self.snakePos[head_pos][1]]
            return pos

        elif not up_down and (0 <= (pos1 + move_int) <= len(self.gameFieldArr) - 1) and \
                (self.gameFieldArr[pos0][pos1 + move_int] == " " or self.gameFieldArr[pos0][pos1 + move_int] == "O"):
            pos = [self.snakePos[head_pos][0], self.snakePos[head_pos][1] + move_int]
            return pos
        return None

    def move_body(self):
        for i in range(len(self.snakePos) - 1):
            if i < len(self.snakePos) - 1:
                self.snakePos[i] = self.snakePos[i + 1]

    def move_snake(self, orientation, up_down, move_int):

        head_pos = len(self.snake) - 1
        self.snake[head_pos] = self.orientation[orientation]
        pos = self.move_dire(up_down, move_int)
        self.moves -= 1

        if pos is None:
            self.lives -= 1
            self.lost_live = True
            return
        if self.moves == 0:
            self.moves = self.reset_moves
            self.lives -= 1
            self.lost_live = True

        temp = self.snakePos[head_pos]
        self.move_body()
        self.snakePos[head_pos] = pos
        if self.gameFieldArr[pos[0]][pos[1]] == 'O':
            self.eaten = True
            self.add_body(temp[0], temp[1])

        self.gameFieldArr[pos[0]][pos[1]] = self.snake[head_pos]
