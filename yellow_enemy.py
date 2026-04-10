import pygame
import math
from enemy_bullet import EnemyBullet

class YellowEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, platforms, enemy_bullets, WIDTH):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 0))  # Yellow
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False
        self.player = player
        self.platforms = platforms
        self.enemy_bullets = enemy_bullets
        self.WIDTH = WIDTH
        self.speed = max(2, player.speed - 2)
        self.jump_power = 18
        self.shoot_cooldown = 0

    def update(self):
        dx = 0
        dist = ((self.player.rect.centerx - self.rect.centerx) ** 2 + (self.player.rect.centery - self.rect.centery) ** 2) ** 0.5
        if dist <= 350:
            if self.player.rect.centerx < self.rect.centerx:
                dx = -self.speed
            elif self.player.rect.centerx > self.rect.centerx:
                dx = self.speed
        self.vel_y += 0.7
        if self.vel_y > 12:
            self.vel_y = 12
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.WIDTH:
            self.rect.right = self.WIDTH
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                if dx < 0:
                    self.rect.left = platform.rect.right
        self.rect.y += int(self.vel_y)
        was_on_ground = self.on_ground
        self.on_ground = False
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        if self.on_ground and abs(self.player.rect.centerx - self.rect.centerx) < 100 and self.player.rect.centery < self.rect.centery:
            self.vel_y = -self.jump_power
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if dist <= 350:
            if self.shoot_cooldown == 0:
                dx = self.player.rect.centerx - self.rect.centerx
                dy = self.player.rect.centery - self.rect.centery
                angle_to_player = math.atan2(dy, dx)
                angles = [angle_to_player,
                          angle_to_player - math.radians(20),
                          angle_to_player + math.radians(20)]
                for ang in angles:
                    enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.centery, ang, self.platforms, self.WIDTH, self.player.rect.bottom)
                    self.enemy_bullets.add(enemy_bullet)
                self.shoot_cooldown = 40
