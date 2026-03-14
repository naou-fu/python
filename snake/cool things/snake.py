import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (40, 40, 40)

# Game settings
FPS = 10  # Snake speed (adjust for difficulty)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("naou Snake Game")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.grow_to = 3
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Check for collision with self
        if new_position in self.positions[1:]:
            return False  # Game over
            
        self.positions.insert(0, new_position)
        
        # Grow the snake if needed
        if len(self.positions) > self.grow_to:
            self.positions.pop()
            
        return True  # Game continues
    
    def render(self, surface):
        for i, pos in enumerate(self.positions):
            # Draw snake segment
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            # Head is darker green
            if i == 0:
                pygame.draw.rect(surface, DARK_GREEN, rect)
                pygame.draw.rect(surface, GREEN, rect, 1)
            else:
                pygame.draw.rect(surface, GREEN, rect)
                pygame.draw.rect(surface, DARK_GREEN, rect, 1)
            
            # Draw eyes on the head
            if i == 0:
                # Determine eye positions based on direction
                dx, dy = self.direction
                eye_size = GRID_SIZE // 5
                
                # Left eye
                left_eye_x = pos[0] * GRID_SIZE + GRID_SIZE // 3
                left_eye_y = pos[1] * GRID_SIZE + GRID_SIZE // 3
                
                # Right eye
                right_eye_x = pos[0] * GRID_SIZE + 2 * GRID_SIZE // 3
                right_eye_y = pos[1] * GRID_SIZE + GRID_SIZE // 3
                
                # Adjust for direction
                if dx == 1:  # Moving right
                    left_eye_x += GRID_SIZE // 6
                    right_eye_x += GRID_SIZE // 6
                    left_eye_y -= GRID_SIZE // 6
                    right_eye_y += GRID_SIZE // 6
                elif dx == -1:  # Moving left
                    left_eye_x -= GRID_SIZE // 6
                    right_eye_x -= GRID_SIZE // 6
                    left_eye_y -= GRID_SIZE // 6
                    right_eye_y += GRID_SIZE // 6
                elif dy == 1:  # Moving down
                    left_eye_x -= GRID_SIZE // 6
                    right_eye_x += GRID_SIZE // 6
                    left_eye_y += GRID_SIZE // 6
                    right_eye_y += GRID_SIZE // 6
                elif dy == -1:  # Moving up
                    left_eye_x -= GRID_SIZE // 6
                    right_eye_x += GRID_SIZE // 6
                    left_eye_y -= GRID_SIZE // 6
                    right_eye_y -= GRID_SIZE // 6
                
                pygame.draw.circle(surface, BLACK, (left_eye_x, left_eye_y), eye_size)
                pygame.draw.circle(surface, BLACK, (right_eye_x, right_eye_y), eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                         random.randint(0, GRID_HEIGHT - 1))
    
    def render(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, 
                          self.position[1] * GRID_SIZE, 
                          GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, (150, 0, 0), rect, 2)
        
        # Draw a shine effect
        shine_rect = pygame.Rect(self.position[0] * GRID_SIZE + GRID_SIZE//4,
                                self.position[1] * GRID_SIZE + GRID_SIZE//4,
                                GRID_SIZE//4, GRID_SIZE//4)
        pygame.draw.ellipse(surface, (255, 200, 200), shine_rect)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GRAY, rect, 1)

def main():
    snake = Snake()
    food = Food()
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                elif not game_over:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
        
        if not game_over:
            # Update snake position
            if not snake.update():
                game_over = True
            
            # Check for food collision
            if snake.get_head_position() == food.position:
                snake.grow_to += 1
                snake.score += 10
                food.randomize_position()
                # Make sure food doesn't appear on snake
                while food.position in snake.positions:
                    food.randomize_position()
        
        # Drawing
        screen.fill(BLACK)
        draw_grid(screen)
        snake.render(screen)
        food.render(screen)
        
        # Draw score
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            game_over_text = font.render("GAME OVER", True, RED)
            score_text = font.render(f"Final Score: {snake.score}", True, WHITE)
            restart_text = small_font.render("Press SPACE to restart", True, WHITE)
            
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))
        
        # Draw instructions
        if not game_over:
            instructions = small_font.render("Use arrow keys to move", True, (150, 150, 150))
            screen.blit(instructions, (WIDTH - instructions.get_width() - 10, HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()