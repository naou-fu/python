import random
import pygame
import json

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dodge the blocks")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
space = (0, 0, 50)
point = 0

class Obstacle:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 80)
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def collide(self, player):
        return self.rect.colliderect(player.rect)

class Player:

    def __init__(self, x, y):
        # Make the hitbox smaller (e.g., 40x40 instead of 60x60)
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 5
        self.last_speedup_score = 0

    def update(self):
        global point
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0 :  # Ліва межа
            self.rect.x -= self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0: # Ліва межа
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < 800:  # Права межа
            self.rect.x += self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800: # Права межа
            self.rect.x += self.speed

        # Increase speed every time score reaches a new multiple of 10
        if point // 10 > self.last_speedup_score:
            self.speed += 1
            self.last_speedup_score = point // 10

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

class Score:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

    def collide(self, player):
        return self.rect.colliderect(player.rect)

    def increase(self):
        global point
        point += 1


# Refactored variable names for clarity
obstacles_left = []
obstacles_right = []
obstacles_center = []
player = Player(375, 500)
score_items = []


obstacle_timer = 0
score_timer = 0
game_over = False
running = True

def reset_game():
    global obstacles_left, obstacles_right, obstacles_center, player, score_items, point, obstacle_timer, score_timer, game_over
    obstacles_left = []
    obstacles_right = []
    obstacles_center = []
    player = Player(375, 500)
    score_items = []
    point = 0
    obstacle_timer = 0
    score_timer = 0
    game_over = False
    player.last_speedup_score = 0
    player.speed = 5

reset_game()

while running:

    if not game_over:
        obstacle_timer += 1
        score_timer += 1
        if obstacle_timer >= 60: # Кожну секунду (60 FPS)
            obstacles_left.append(Obstacle(random.randint(0, 365), -50))
            obstacles_right.append(Obstacle(random.randint(376, 750), -50))
            obstacles_center.append(Obstacle(random.randint(0, 750), -50))
            obstacle_timer = 0

        if score_timer >= 120:
            score_items.append(Score(random.randint(0, 750), -50))
            score_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    reset_game()

        screen.fill(space)
        player.draw(screen)
        player.update()

        # Safely remove collected or off-screen score items
        for sc in score_items[:]:
            sc.update()
            sc.draw(screen)
            if sc.collide(player):
                sc.increase()
                score_items.remove(sc)
            elif sc.rect.top > 600:
                score_items.remove(sc)

        # Safely remove off-screen obstacles and check collision
        for ob in obstacles_left[:]:
            ob.update()
            ob.draw(screen)
            if ob.rect.top > 600:
                obstacles_left.remove(ob)
            elif ob.collide(player):
                game_over = True

        for ob in obstacles_right[:]:
            ob.update()
            ob.draw(screen)
            if ob.rect.top > 600:
                obstacles_right.remove(ob)
            elif ob.collide(player):
                game_over = True

        for ob in obstacles_center[:]:
            ob.update()
            ob.draw(screen)
            if ob.rect.top > 600:
                obstacles_center.remove(ob)
            elif ob.collide(player):
                game_over = True

        # Draw score and player speed on screen
        score_text = font.render(f"Score: {point}", True, (255, 255, 0))
        speed_text = font.render(f"Speed: {player.speed}", True, (0, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(speed_text, (10, 50))

        pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)

        if game_over:
            over_text = font.render("Game Over! Press R to restart", True, (255, 0, 0))
            screen.blit(over_text, (200, 300))

        pygame.display.flip()
        clock.tick(60)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
        screen.fill(space)
        over_text = font.render("Game Over! Press R to restart", True, (255, 0, 0))
        score_text = font.render(f"Score: {point}", True, (255, 255, 0))
        speed_text = font.render(f"Speed: {player.speed}", True, (0, 255, 255))
        screen.blit(over_text, (200, 300))
        screen.blit(score_text, (10, 10))
        screen.blit(speed_text, (10, 50))
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
exit()