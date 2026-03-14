import pygame
import sys
import math
import random


# Initialize pygame
#nl
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("naou Bouncing Balls in a Circle")
clock = pygame.time.Clock()

# Colors
BACKGROUND = (10, 15, 30)
CIRCLE_COLOR = (40, 60, 100)
CIRCLE_BORDER = (70, 130, 180)
BUTTON_BG = (50, 60, 80)
BUTTON_HOVER = (70, 90, 120)
BUTTON_TEXT = (220, 230, 250)
TEXT_COLOR = (200, 210, 230)
SPEED_COLORS = [
    (255, 100, 100),  # Red — slow
    (255, 200, 100),  # Orange — medium
    (100, 255, 100),  # Green — fast
]

# Circle parameters (centered)
CIRCLE_RADIUS = 220
CIRCLE_CENTER = (WIDTH // 2, HEIGHT // 2)

# Ball class
class Ball:
    def __init__(self, radius=10):
        self.radius = radius
        # Start inside the circle
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, CIRCLE_RADIUS - self.radius - 5)
        self.x = CIRCLE_CENTER[0] + dist * math.cos(angle)
        self.y = CIRCLE_CENTER[1] + dist * math.sin(angle)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
    
    def update(self, speed_factor):
        # Update position with speed scaling
        self.x += self.vx * speed_factor
        self.y += self.vy * speed_factor
        
        # Calculate distance from center
        dx = self.x - CIRCLE_CENTER[0]
        dy = self.y - CIRCLE_CENTER[1]
        distance = math.hypot(dx, dy)
        
        # If ball hits the circular boundary
        if distance + self.radius > CIRCLE_RADIUS:
            # Normalize direction vector
            if distance > 0:
                nx = dx / distance
                ny = dy / distance
            else:
                nx, ny = 1, 0  # fallback
            
            # Reflect velocity vector: v' = v - 2(v·n)n
            dot = self.vx * nx + self.vy * ny
            self.vx -= 2 * dot * nx
            self.vy -= 2 * dot * ny
            
            # Reposition ball to boundary to prevent sticking
            new_dist = CIRCLE_RADIUS - self.radius
            self.x = CIRCLE_CENTER[0] + nx * new_dist
            self.y = CIRCLE_CENTER[1] + ny * new_dist
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Add shine for visual appeal
        shine_pos = (int(self.x - self.radius/3), int(self.y - self.radius/3))
        pygame.draw.circle(surface, (255, 255, 255, 100), shine_pos, self.radius//3)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        self.font = pygame.font.SysFont(None, 28)
    
    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_BG
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (100, 130, 180), self.rect, 2, border_radius=8)
        
        text_surf = self.font.render(self.text, True, BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                self.action()

# Create initial balls
balls = [Ball() for _ in range(3)]
speed_factor = 1.0  # 1.0 = normal speed

# Create buttons
button_width, button_height = 140, 45
gap = 15
start_x = 30
start_y = HEIGHT - button_height - 30

buttons = [
    Button(start_x, start_y, button_width, button_height, "Add Ball", lambda: balls.append(Ball())),
    Button(start_x + button_width + gap, start_y, button_width, button_height, "Remove Ball", lambda: balls.pop() if balls else None),
    Button(start_x + 2*(button_width + gap), start_y, button_width, button_height, "Speed +", lambda: increase_speed()),
    Button(start_x + 3*(button_width + gap), start_y, button_width, button_height, "Speed -", lambda: decrease_speed()),
]

def increase_speed():
    global speed_factor
    speed_factor = min(3.0, speed_factor + 0.2)

def decrease_speed():
    global speed_factor
    speed_factor = max(0.2, speed_factor - 0.2)

# Font
font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 24)

# Main loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)
    
    # Update button hover states
    for button in buttons:
        button.check_hover(mouse_pos)
    
    # Update balls
    for ball in balls:
        ball.update(speed_factor)
    
    # Drawing
    screen.fill(BACKGROUND)
    
    # Draw outer decorative circles
    for i in range(3):
        radius = CIRCLE_RADIUS + 10 + i*3
        alpha = 30 - i*10
        pygame.draw.circle(screen, (*CIRCLE_BORDER, alpha), CIRCLE_CENTER, radius, 1)
    
    # Draw main boundary circle
    pygame.draw.circle(screen, CIRCLE_BORDER, CIRCLE_CENTER, CIRCLE_RADIUS, 3)
    pygame.draw.circle(screen, CIRCLE_COLOR, CIRCLE_CENTER, CIRCLE_RADIUS - 2)
    
    # Draw balls
    for ball in balls:
        ball.draw(screen)
    
    # Draw UI panel background
    pygame.draw.rect(screen, (20, 25, 40, 200), (0, HEIGHT - 80, WIDTH, 80))
    pygame.draw.line(screen, (60, 80, 110), (0, HEIGHT - 80), (WIDTH, HEIGHT - 80), 2)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)
    
    # Draw info text
    info_text = font.render(f"Balls: {len(balls)}", True, TEXT_COLOR)
    screen.blit(info_text, (WIDTH - info_text.get_width() - 20, 20))
    
    # Speed indicator
    speed_text = font.render("Speed:", True, TEXT_COLOR)
    screen.blit(speed_text, (WIDTH - 200, 60))
    
    # Speed bar
    bar_x, bar_y = WIDTH - 120, 65
    bar_width, bar_height = 100, 12
    pygame.draw.rect(screen, (40, 50, 70), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
    
    # Colored speed bar segment
    speed_pct = (speed_factor - 0.2) / (3.0 - 0.2)  # Normalize 0.2–3.0 to 0–1
    segment_width = int(bar_width * speed_pct)
    color_idx = min(2, int(speed_pct * 3))
    pygame.draw.rect(screen, SPEED_COLORS[color_idx], (bar_x, bar_y, segment_width, bar_height), border_radius=4)
    
    # Speed value
    val_text = small_font.render(f"{speed_factor:.1f}x", True, TEXT_COLOR)
    screen.blit(val_text, (bar_x + bar_width + 5, bar_y - 2))
    
    # Title
    title = font.render("Bouncing Balls in a Circle", True, (100, 180, 255))
    screen.blit(title, (20, 20))
    
    # Instructions
    instr = small_font.render("Click buttons below to control simulation", True, (120, 150, 190))
    screen.blit(instr, (20, 60))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()