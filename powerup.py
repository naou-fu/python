import pygame

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 0), (12, 12), 12)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = 0

    def update(self, platforms=None, *args, **kwargs):
        # Gravity
        self.vel_y += 0.7
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += int(self.vel_y)
        # Platform collision
        if platforms:
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
