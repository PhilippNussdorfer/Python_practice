import numpy
import gym
from gym.spaces import box

from MoveSnake import game


class Snake:
    """
    is the snake class of with its variables and methods
    """
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
        """
        creates a list of spaces with numpy fill
        :return:
        """
        self.gameFieldArr = numpy.full((self.game_field_size, self.game_field_size), " ")

    def reset_snake(self):
        """
        resets the snake to only its head and start position
        :return:
        """
        self.snake = [self.orientation[2]]
        self.snakePos = [[0, 0]]

    def add_body(self, pos0, pos1):
        """
        adds a new # segment to the snake and its position in the list snake and snakePos
        :param pos0: pos0 of the head (or x) before it gets a new pos
        :param pos1: pos1 of the head (or y) before it gets a new pos
        :return:
        """
        self.snake.insert(0, '#')
        self.snakePos.insert(0, [pos0, pos1])

    def move_body(self):
        """
        a body part of the snake gets the pos of the part after it and that goes on until it reaches the head
        :return:
        """
        for i in range(len(self.snakePos) - 1):
            if i < len(self.snakePos) - 1:
                self.snakePos[i] = self.snakePos[i + 1]

    def move_dire(self, up_down, move_int):
        """
        checks if the next tile is on the game field or an apple or a free tile
        if true it will return the next pos of the head else none
        :param up_down: bool if the input was w or s then it is true else its false
        :param move_int: is the direction w = -1 (up) s = 1 (down) a = -1 (left) d = 1 (right)
        :return:
        """
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

    def move_snake(self, orientation, up_down, move_int):
        """
        calls move_dire(up_down move_int) to get the new pos of the head if it returns none the head will not move and
        instead the snake losses a live or if the moves of the snake reaches 0 it will lose a live because of hunger
        else it saves the old pos in a temp variable if the snake eats an apple the temp value will be used to add a new
         body with the pos saved in temp element to the snake
        and moves the snake normal and will add the body part a bit later on the screen.
        :param orientation: the orientation of the head 0:^ 1:> 2:v 3:<
        :param up_down: the body moves up or down = True else = False
        :param move_int:  move_int: is the direction w = -1 (up) s = 1 (down) a = -1 (left) d = 1 (right)
        :return:
        """
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
