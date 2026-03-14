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
platform5 = GamePlatform(400, HEIGHT - 600, 200, 20)
platform6 = GamePlatform(900, HEIGHT - 150, 180, 20)
platform7 = GamePlatform(1300, HEIGHT - 400, 220, 20)
platform8 = GamePlatform(1700, HEIGHT - 600, 180, 20)
platform9 = GamePlatform(100, HEIGHT - 300, 150, 20)
platform10 = GamePlatform(800, HEIGHT - 700, 220, 20)
platform11 = GamePlatform(1400, HEIGHT - 100, 160, 20)
platform12 = GamePlatform(500, HEIGHT - 800, 200, 20)

platforms.add(ground, platform1, platform2, platform3, platform4, platform5, platform6, platform7,
               platform8, platform9, platform10, platform11, platform12)
all_sprites.add(ground, platform1, platform2, platform3, platform4, platform5, platform6, platform7,
                platform8, platform9, platform10, platform11, platform12)

# Create enemies
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

def main():
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
