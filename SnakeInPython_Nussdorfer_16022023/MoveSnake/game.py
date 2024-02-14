import random
import sys

import Snake
import pygame
import threading


class Game:
    """
    is the game class with its variables and methods
    """
    def __init__(self, game_field_size, width=600, height=600):
        pygame.init()
        self.score = 0
        self.applePos = []
        self.win = False
        self.game_over = False
        self.snake = Snake.Snake(game_field_size)
        self.is_apple = True
        self.boarder_c = [0, 0, 0]
        self.tile_c = [160, 160, 160]
        self.text_c = [247, 0, 255]
        self.apple_c = [255, 0, 0]
        self.font = pygame.font.SysFont('Comic Sans MS', 32)
        self.width = width
        self.height = height
        self.val2color = {" ": self.tile_c, "#": self.snake.body_color, "O": self.apple_c,
                          "v": self.snake.head_color, "^": self.snake.head_color, "<": self.snake.head_color,
                          ">": self.snake.head_color, "*": self.boarder_c}
        self.clock = pygame.time.Clock()
        self.run_game = True
        self.action = ""
        self.score_file = "Scores.txt"

    def update(self):
        """
        update resets the array on spaces
        will try and set the apple if there is no apple the method will set a new apple where no snake part is
        if the apple was eaten then the method will start the method apple_eaten and will set eaten to False
        :return:
        """
        for i in range(len(self.snake.gameFieldArr)):
            for j in range(len(self.snake.gameFieldArr)):
                self.snake.gameFieldArr[i][j] = " "

        self.set_apple()
        if self.snake.eaten:
            self.apple_eaten()
            self.snake.eaten = False
        for i in range(len(self.snake.snakePos)):
            self.snake.gameFieldArr[self.snake.snakePos[i][0]][self.snake.snakePos[i][1]] = self.snake.snake[i]

    def set_apple(self):
        """
        will set the apple on a new random pos where no snake part is
        :return:
        """
        if self.is_apple:
            self.applePos = [random.randint(0, len(self.snake.gameFieldArr) - 1), random.randint(0, len(self.snake.gameFieldArr) - 1)]
            while True:
                if self.applePos not in self.snake.snakePos:
                    break
                self.applePos = [random.randint(0, len(self.snake.gameFieldArr) - 1), random.randint(0, len(self.snake.gameFieldArr) - 1)]
            self.is_apple = False
        self.snake.gameFieldArr[self.applePos[0]][self.applePos[1]] = "O"

    def apple_eaten(self):
        """
        when the apple is eaten it will set the variable is_apple to True, will start the set_apple methode
        will set the moves the snake has to its starting moves and adds 10 points to the score
        :return:
        """
        self.is_apple = True
        self.set_apple()
        self.snake.moves = self.snake.reset_moves
        self.score += 10

    def handle_usr_input(self, usr_input):
        """
        handles the inputs of the player and the orientation with the new input
        :param usr_input:
        :return:
        """

        if usr_input.lower() == "w":
            self.snake.move_snake(0, True, -1)

        if usr_input.lower() == "s":
            self.snake.move_snake(2, True, 1)

        if usr_input.lower() == "a":
            self.snake.move_snake(3, False, -1)

        if usr_input.lower() == "d":
            self.snake.move_snake(1, False, 1)

    def test_for_win(self):
        """
        tests if the player has won the game
        sets win on True
        :return:
        """
        if any(" " in sublist for sublist in self.snake.gameFieldArr) or any("O" in sublist for sublist in self.snake.gameFieldArr):
            self.win = False
        else:
            self.win = True
            self.score += 50

    def reset(self):
        """
        resets the game when the player makes the decision to play again
        :return:
        """
        self.snake.moves = (len(self.snake.gameFieldArr) * 2) - 1
        self.snake.reset_snake()
        self.snake.lives = 3
        self.score = 0
        self.game_over = False
        self.win = False
        self.action = ""

    def render_text_from_center(self, text, font, color, x, y, screen, allowed_width):
        """
        adds a test to the cords on the x and y position
        :param text: str
        :param font: font of the text
        :param color: RGB color of the text
        :param x: int: cords
        :param y: int: cords
        :param screen: pygame screen of the game
        :param allowed_width: int: max width of the text
        :return:
        """

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
            tx = x - fw/2
            ty = y + y_offset

            font_surface = font.render(line, True, color)
            screen.blit(font_surface, (tx, ty))

            y_offset += fh

    def action_listener(self):
        """
        the action_listener will start listen for inputs with pygame and update the action when it got an input
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                self.run_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.run_game = False
                if event.key == pygame.K_w and self.action != "s":
                    self.action = "w"
                if event.key == pygame.K_s and self.action != "w":
                    self.action = "s"
                if event.key == pygame.K_d and self.action != "a":
                    self.action = "d"
                if event.key == pygame.K_a and self.action != "d":
                    self.action = "a"

    def render(self):
        """
        renders the game with pygame
        will start a screen where the game is visible
        :return:
        """
        screen = pygame.display.set_mode([self.width, self.height])
        #action_thread = threading.Thread(target=self.action_listener)
        #action_thread.start()

        while self.run_game:

            self.action_listener()
            self.handle_usr_input(self.action)
            self.update()
            self.test_for_win()
            for i in range(len(self.snake.gameFieldArr)):
                for j in range(len(self.snake.gameFieldArr)):
                    pygame.draw.rect(screen, self.val2color[self.snake.gameFieldArr[i][j]], (j * 45, i * 45, 45, 45))

            self.render_text_from_center("Moves:{}  Score:{}  Lives:{}".format(self.snake.moves, self.score, self.snake.lives), self.font, self.text_c, self.width / 2, self.height - 100, screen, self.width)
            if self.snake.lives == 0:
                self.game_over = True

            if self.win or self.game_over:
                self.run_game = False

            pygame.display.update()
            screen.fill(self.boarder_c)
            self.clock.tick(5)

            if not self.run_game:
                self.save_score()
                sorted_score_list = self.get_high_score()
                run = True
                while run:
                    self.render_text_from_center("Your score is: {}".format(self.score), self.font, self.text_c, self.width / 2, 20, screen, self.width)
                    if int(self.score) > int(sorted_score_list[1][0]):
                        self.render_text_from_center("New High Score: {} !!!".format(sorted_score_list[0][0]), self.font,
                                                     self.text_c, self.width / 2, 60, screen, self.width)
                    else:
                        self.render_text_from_center("High Score: {}".format(sorted_score_list[0][0]), self.font, self.text_c, self.width / 2, 60, screen, self.width)
                    self.render_text_from_center("Enter y to start a new game or n to stop the game", self.font, self.text_c, self.width / 2, self.height / 3, screen, self.width)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                run = False
                            if event.key == pygame.K_y:
                                self.reset()
                                self.run_game = True
                                break
                            if event.key == pygame.K_n:
                                run = False
                    if self.run_game:
                        #action_thread_sec = threading.Thread(target=self.action_listener)
                        #action_thread_sec.start()
                        break
                if not run:
                    sys.exit()

    def sort_after(self, list_row):
        """
        returns value of the first list element
        :param list_row:
        :return:
        """
        return int(list_row[0])

    def get_high_score(self):
        """
        sorts a list of scores from the first element in the list
        returns a sorted list where the biggest score is tob and the lowest bottom
        :return:
        """
        sort_list = []
        with open(self.score_file, "r") as all_scores:

            for score in all_scores:
                score = score.strip()
                sort_list.append(score.split(";"))

        sort_list.sort(key=self.sort_after, reverse=True)
        return sort_list

    def save_score(self):
        """
        Saves the scores in a txt file
        :return:
        """
        file_write = open(self.score_file, "a")
        file_write.write("{};{};{}\n".format(self.score, self.snake.lives, len(self.snake.snake)))
        file_write.close()

    def set_start(self):
        """
        initializes the start of the game
        :return:
        """
        self.snake.create_game_field()
        head_pos = len(self.snake.snake) - 1
        self.set_apple()
        self.snake.gameFieldArr[self.snake.snakePos[head_pos][0]][self.snake.snakePos[head_pos][1]] = self.snake.snake[head_pos]

        render_thread = threading.Thread(target=self.render)
        render_thread.start()
