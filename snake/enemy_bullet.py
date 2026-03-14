import pygame
import math

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle_rad, platforms, WIDTH, HEIGHT):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7
        self.angle_rad = angle_rad
        self.dx = math.cos(angle_rad) * self.speed
        self.dy = math.sin(angle_rad) * self.speed
        self.platforms = platforms
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def update(self):
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                self.kill()
                return
        if (self.rect.right < 0 or self.rect.left > self.WIDTH or
            self.rect.bottom < 0 or self.rect.top > self.HEIGHT):
            self.kill()
