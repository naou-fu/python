
'''
This file has been intentionally left blank. All game logic has been moved to main.py.
'''


import pygame
import sys
import math

from player import Player
from bullet import Bullet
from game_platform import GamePlatform
from enemy_bullet import EnemyBullet
from enemy import Enemy
from yellow_enemy import YellowEnemy
from powerup import Powerup
from run_game import run_game

import pygame
import sys

# Initialize Pygame
pygame.init()




# Screen settings - use current display resolution
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Shooter")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)













# Create groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()


player = Player(100, HEIGHT - 150, BLUE)
all_sprites.add(player)



# Create platforms
ground = GamePlatform(0, HEIGHT - 40, WIDTH, 40)
platform1 = GamePlatform(200, HEIGHT - 200, 300, 20)
platform2 = GamePlatform(600, HEIGHT - 350, 250, 20)
platform3 = GamePlatform(1000, HEIGHT - 500, 300, 20)
platform4 = GamePlatform(1500, HEIGHT - 250, 200, 20)

# Create enemies

# Initial enemy spawn positions
enemy_spawn_positions = [
    (600, HEIGHT - 80),
    (1200, HEIGHT - 300),
    (300, HEIGHT - 500),
    (1000, HEIGHT - 200)
]
for pos in enemy_spawn_positions:
    e = Enemy(pos[0], pos[1], player, platforms, enemy_bullets, WIDTH)
    enemies.add(e)
    all_sprites.add(e)






# Main game loop with modular run_game
while True:
    run_game(
        player,
        all_sprites,
        platforms,
        enemies,
        enemy_bullets,
        WIDTH,
        HEIGHT,
        screen,
        clock,
        WHITE,
        RED,
        6,  # max_health
        Enemy,
        EnemyBullet
    )


