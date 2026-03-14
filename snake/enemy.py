import pygame
import math
from enemy_bullet import EnemyBullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, platforms, enemy_bullets, WIDTH):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 140, 0))  # Orange
        self.max_health = 2
        self.health = self.max_health
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False
        self.player = player
        self.platforms = platforms
        self.enemy_bullets = enemy_bullets
        self.WIDTH = WIDTH
        self.speed = max(1, player.speed - 4)
        self.jump_power = 16
        self.shoot_cooldown = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.image.get_at((0,0)) == (255, 140, 0, 255):  # Orange enemy
            # Draw health bar above enemy
            bar_width = 30
            bar_height = 5
            x = self.rect.x + 5
            y = self.rect.y - 10
            health_ratio = self.health / self.max_health
            pygame.draw.rect(surface, (128,128,128), (x, y, bar_width, bar_height))
            pygame.draw.rect(surface, (0,255,0), (x, y, int(bar_width * health_ratio), bar_height))

    def take_hit(self):
        if self.health > 0:
            self.health -= 1
        if self.health <= 0:
            self.kill()

    def update(self):
        dx = 0
        dist = ((self.player.rect.centerx - self.rect.centerx) ** 2 + (self.player.rect.centery - self.rect.centery) ** 2) ** 0.5
        if dist <= 300:
            if self.player.rect.centerx < self.rect.centerx:
                dx = -self.speed
            elif self.player.rect.centerx > self.rect.centerx:
                dx = self.speed
        self.vel_y += 0.7
        if self.vel_y > 10:
            self.vel_y = 10
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
        if self.on_ground and abs(self.player.rect.centerx - self.rect.centerx) < 80 and self.player.rect.centery < self.rect.centery:
            self.vel_y = -self.jump_power
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        dist = ((self.player.rect.centerx - self.rect.centerx) ** 2 + (self.player.rect.centery - self.rect.centery) ** 2) ** 0.5
        if dist <= 300:
            if self.shoot_cooldown == 0:
                dx = self.player.rect.centerx - self.rect.centerx
                dy = self.player.rect.centery - self.rect.centery
                angle_to_player = math.atan2(dy, dx)
                bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle_to_player, self.platforms, self.WIDTH, self.player.rect.bottom)
                self.enemy_bullets.add(bullet)
                self.shoot_cooldown = 60
