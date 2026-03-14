import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, BLUE):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False
        self.speed = 5
        self.jump_power = 16
        self.bullets = pygame.sprite.Group()
        self.facing_right = True
        self.shoot_cooldown = 0
        self.jump_buffer = 0
        self.shoot_buffer = 0
        self.jumps_left = 2

    def update(self, platforms, WIDTH):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
            self.facing_right = True
        self.vel_y += 0.7
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1920:
            self.rect.right = 1920
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                if dx < 0:
                    self.rect.left = platform.rect.right
        self.rect.y += int(self.vel_y)
        was_on_ground = self.on_ground
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        if self.on_ground and not was_on_ground:
            self.jumps_left = 2
        if self.on_ground and not was_on_ground and self.jump_buffer > 0:
            self.vel_y = -self.jump_power
            self.jump_buffer = 0
        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        self.bullets.update(platforms, WIDTH)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.shoot_cooldown == 0 and self.shoot_buffer > 0:
            from bullet import Bullet
            bullet = Bullet(self.rect.centerx, self.rect.top, self.facing_right)
            self.bullets.add(bullet)
            self.shoot_cooldown = 15
            self.shoot_buffer = 0
        if self.shoot_buffer > 0:
            self.shoot_buffer -= 1

    def jump(self):
        if self.jumps_left > 0:
            self.vel_y = -self.jump_power
            self.jumps_left -= 1
            self.jump_buffer = 0
        else:
            self.jump_buffer = 9

    def shoot(self):
        if self.shoot_cooldown == 0:
            from bullet import Bullet
            bullet = Bullet(self.rect.centerx, self.rect.top, self.facing_right)
            self.bullets.add(bullet)
            self.shoot_cooldown = 15
            self.shoot_buffer = 0
        else:
            self.shoot_buffer = 9
