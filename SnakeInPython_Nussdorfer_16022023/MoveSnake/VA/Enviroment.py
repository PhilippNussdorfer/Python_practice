import random
import sys
import time
from abc import ABC
from collections import deque
import pygame
import Snake
import gymnasium as gym
from gym import Env
from gym.spaces import Box, Discrete
import numpy as np
from gymnasium import spaces


def render_text_from_center(text, font, color, x, y, screen, allowed_width):
    words = text.split()

    lines = []
    while len(words) > 0:
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        line = ' '.join(line_words)
        lines.append(line)

    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)
        tx = x - fw / 2
        ty = y + y_offset

        font_surface = font.render(line, True, color)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh


class SnakeEnv(Env, ABC):
    """Custom Environment that follows gym interface."""

    metadata = {"render.modes": ["human"]}

    def __init__(self):
        super().__init__()
        self.done_win = False
        pygame.init()
        self.seed = None
        self.reward = 0
        self.game_field_size = 15
        self.snake_len_goal = self.game_field_size * 2
        self.done = False
        self.snake = Snake.Snake(self.game_field_size)
        self.score = 0
        self.game_over = False
        self.win = False
        self.action = ""
        self.apple_pos = []
        self.is_apple = True
        self.prv_actions = []
        self.observation = []
        self.penalty = 0
        self.mul = 45
        self.dimensions = self.game_field_size * self.mul
        self.screen = pygame.display.set_mode([self.dimensions, self.dimensions])
        self.boarder_c = [0, 0, 0]
        self.tile_c = [160, 160, 160]
        self.text_c = [247, 0, 255]
        self.apple_c = [255, 0, 0]
        self.val2color = {" ": self.tile_c, "#": self.snake.body_color, "O": self.apple_c,
                          "v": self.snake.head_color, "^": self.snake.head_color, "<": self.snake.head_color,
                          ">": self.snake.head_color, "*": self.boarder_c}
        self.snake_pos_x = []
        self.snake_pos_y = []
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = Discrete(4)
        # Example for using image as input (channel-first; channel-last also works):
        # self.observation_space = Box(low=-500, high=500,
        #                             shape=(5 + self.snake_len_goal,), dtype=int)
        self.observation_space = Box(low=-500, high=500,
                                     shape=(6 + ((self.game_field_size * self.game_field_size) * 2),), dtype=int)

    def set_apple(self):
        if self.is_apple:
            self.apple_pos = [random.randint(0, len(self.snake.gameFieldArr) - 1),
                              random.randint(0, len(self.snake.gameFieldArr) - 1)]
            while True:
                if self.apple_pos[0] != 0 and self.apple_pos[1] != 0 and self.apple_pos not in self.snake.snakePos:
                    break
                self.apple_pos = [random.randint(0, len(self.snake.gameFieldArr) - 1),
                                  random.randint(0, len(self.snake.gameFieldArr) - 1)]
            self.is_apple = False
        self.snake.gameFieldArr[self.apple_pos[0]][self.apple_pos[1]] = "O"

    def test_for_win(self):
        if any(" " in sublist for sublist in self.snake.gameFieldArr) or any(
                "O" in sublist for sublist in self.snake.gameFieldArr):
            self.win = False
        else:
            self.win = True
            self.score += 2500

    def update(self):
        for i in range(len(self.snake.gameFieldArr)):
            for j in range(len(self.snake.gameFieldArr)):
                self.snake.gameFieldArr[i][j] = " "

        self.set_apple()
        if self.snake.eaten:
            self.apple_eaten()
            self.snake.eaten = False
        for i in range(len(self.snake.snakePos)):
            self.snake.gameFieldArr[self.snake.snakePos[i][0]][self.snake.snakePos[i][1]] = self.snake.snake[i]

    def apple_eaten(self):
        self.is_apple = True
        self.set_apple()
        self.snake.moves = self.snake.reset_moves
        self.score += 10

    def handle_action(self, action):

        if action == 0 and action != 1:
            self.snake.move_snake(0, True, -1)

        if action == 1 and action != 0:
            self.snake.move_snake(2, True, 1)

        if action == 2 and action != 3:
            self.snake.move_snake(3, False, -1)

        if action == 3 and action != 2:
            self.snake.move_snake(1, False, 1)

    def render_view(self, action, slow=False):

        self.handle_action(action)
        self.update()
        self.test_for_win()
        for i in range(len(self.snake.gameFieldArr)):
            for j in range(len(self.snake.gameFieldArr)):
                pygame.draw.rect(self.screen, self.val2color[self.snake.gameFieldArr[i][j]],
                                 (j * self.mul, i * self.mul, self.mul, self.mul))

        render_text_from_center("Moves:{}  Score:{}  Lives:{}".format(self.snake.moves, self.score, self.snake.lives),
                                pygame.font.SysFont('Comic Sans MS', 32), self.text_c, self.dimensions / 2,
                                self.dimensions - 100, self.screen, self.dimensions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if slow:
            time.sleep(0.1)

        if self.snake.lives <= 0:
            self.game_over = True

        if self.game_over:
            self.done = True

        if self.win:
            self.done_win = True

        pygame.display.update()
        self.screen.fill(self.boarder_c)

        if self.done:
            render_text_from_center("Your score is: {}".format(self.score), pygame.font.SysFont('Comic Sans MS', 32),
                                    self.text_c, self.dimensions / 2, 20, self.screen, self.dimensions)
            pygame.display.update()

        if slow:
            time.sleep(0.2)

    def step(self, action, slow=False):
        self.prv_actions.append(action)
        self.render_view(action, slow=slow)

        # if self.snake.moves % 5 == 0:
            # self.penalty += 0.4
        if self.snake.lost_live:
            self.penalty += 4
            self.snake.lost_live = False

        if self.done:
            self.reward = -100
        elif self.done_win:
            self.reward = self.score * 10
        else:
            self.reward = ((self.score * 1.15) + len(self.snake.snake)) # - self.penalty

        info = {}

        head_x = self.snake.snakePos[len(self.snake.snakePos) - 1][0]
        head_y = self.snake.snakePos[len(self.snake.snakePos) - 1][1]

        # apple_delta_x = head_x - self.apple_pos[0]
        # apple_delta_y = head_y - self.apple_pos[1]

        self.snake_pos_x = []
        self.snake_pos_y = []
        for i in range(self.game_field_size * self.game_field_size):
            self.snake_pos_x.append(-1)
            self.snake_pos_y.append(-1)

        for xy in self.snake.snakePos:
            self.snake_pos_x.append(xy[0])
            self.snake_pos_y.append(xy[1])
            self.snake_pos_x.pop(0)
            self.snake_pos_y.pop(0)

        self.observation = [head_x, head_y, self.apple_pos[0], self.apple_pos[1], self.snake.moves, self.snake.lives] + list(self.snake_pos_x) + list(
            self.snake_pos_y)
        self.observation = np.array(self.observation)

        return self.observation, self.reward, self.done, info

    def reset(self):
        self.done_win = False
        self.done = False
        self.is_apple = True
        self.snake.create_game_field()
        self.snake.moves = (len(self.snake.gameFieldArr) * 2) - 1
        self.snake.lives = 3
        self.score = 0
        self.reward = 0
        self.game_over = False
        self.win = False
        self.action = ""
        self.snake.reset_snake()
        self.set_apple()
        self.snake_pos_x = []
        self.snake_pos_y = []
        self.penalty = 0

        # head_y, head_x, apple_x, apple_y, snake_length, previous_moves
        head_x = self.snake.snakePos[len(self.snake.snakePos) - 1][0]
        head_y = self.snake.snakePos[len(self.snake.snakePos) - 1][1]

        # apple_delta_x = head_x - self.apple_pos[0]
        # apple_delta_y = head_y - self.apple_pos[1]

        # self.prv_actions = deque(maxlen=goal)
        # for i in range(goal):
        #    self.prv_actions.append(-1)

        for i in range(self.game_field_size * self.game_field_size):
            self.snake_pos_x.append(-1)
            self.snake_pos_y.append(-1)

        for xy in self.snake.snakePos:
            self.snake_pos_x.append(xy[0])
            self.snake_pos_y.append(xy[1])
            self.snake_pos_x.pop(0)
            self.snake_pos_y.pop(0)

        self.observation = [head_x, head_y, self.apple_pos[0], self.apple_pos[1], self.snake.moves, self.snake.lives] + list(self.snake_pos_x) + list(
            self.snake_pos_y)
        self.observation = np.array(self.observation)

        return self.observation  # reward, done, info can't be included

#    def render(self, mode='human'):

#    def close(self):
