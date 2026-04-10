import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, right=True, RED=(255,0,0)):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10 if right else -10

    def update(self, platforms, WIDTH):
        self.rect.x += self.speed
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.kill()
                return
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
