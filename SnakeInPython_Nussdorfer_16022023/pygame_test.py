import pygame
import random

from pygame.locals import (K_UP, K_DOWN, K_RIGHT, K_LEFT, K_ESCAPE, QUIT, KEYDOWN)


WIDTH = 1200
HEIGHT = 900


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_key):
        if pressed_key[K_UP]:
            self.rect.move_ip(0, -4)
        if pressed_key[K_DOWN]:
            self.rect.move_ip(0, 4)
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-4, 0)
        if pressed_key[K_RIGHT]:
            self.rect.move_ip(4, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 80, 80))
        self.rect = self.surf.get_rect(center=(random.randint(WIDTH + 20, WIDTH + 100), random.randint(0, HEIGHT),))
        self.speed = random.randint(2, 7)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 250)

player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

run = True
clock = pygame.time.Clock()

while run:

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
        elif event.type == QUIT:
            run = False
        elif event.type == ADD_ENEMY:
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)

    pressed_key = pygame.key.get_pressed()
    player.update(pressed_key)

    enemies.update()

    screen.fill((0, 0, 0))
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollide(player, enemies, True):
        player.kill()
        run = False

    screen.blit(player.surf, player.rect)
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
