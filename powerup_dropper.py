import pygame
import random
from powerup import Powerup

class PowerupDropper:
    def __init__(self, all_sprites, powerups):
        self.all_sprites = all_sprites
        self.powerups = powerups

    def drop_powerups_on_wave(self, enemy_group):
        if len(enemy_group) == 0:
            return
        chosen = random.sample(list(enemy_group), min(2, len(enemy_group)))
        for enemy in chosen:
            px = enemy.rect.centerx
            py = enemy.rect.bottom + 10
            p = Powerup(px, py)
            self.powerups.add(p)
            self.all_sprites.add(p)
