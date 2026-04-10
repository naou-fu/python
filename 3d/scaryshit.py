
import pygame
import math
import random
import os
from collections import deque

# Initialize pygame
pygame.init()

# Optional sound/mixer setup: looks for a `sounds` folder next to this file
SOUND_ENABLED = False
try:
    pygame.mixer.init()
    SOUND_ENABLED = True
except Exception:
    SOUND_ENABLED = False

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Maze Escape")
clock = pygame.time.Clock()
colors1 = [(187, 12, 220), (0, 0, 0)]

# Sound helper: try to load sound files from `sounds/` folder next to this file
SOUND_DIR = os.path.join(os.path.dirname(__file__), "sounds")
def _load_sound(*names):
    if not SOUND_ENABLED:
        return None
    for name in names:
        path = os.path.join(SOUND_DIR, name)
        if os.path.exists(path):
            try:
                return pygame.mixer.Sound(path)
            except Exception:
                pass
    return None

# Load named sounds (fall back to None if files missing)
start_sound = _load_sound('start.wav', 'start.ogg')
swing_sound = _load_sound('swing.wav', 'swing.ogg')
slash_sound = _load_sound('slash.wav', 'slash.ogg')
defend_sound = _load_sound('defend.wav', 'defend.ogg')
win_sound = _load_sound('win.wav', 'win.ogg')
jumpscare_sound = _load_sound('jumpscare.wav', 'jumpscare.ogg')

# Background music (optional)
bg_music_path = None
if SOUND_ENABLED and os.path.isdir(SOUND_DIR):
    for candidate in ('395803__klankbeeld__horror-170601_1190.wav'):
        p = os.path.join(SOUND_DIR, candidate)
        if os.path.exists(p):
            bg_music_path = p
            break
    if bg_music_path:
        try:
            pygame.mixer.music.load(bg_music_path)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except Exception:
            pass
# Colors
BACKGROUND = (20, 20, 40)
WALL_COLOR = random.choice(colors1)
FLOOR_COLOR = (40, 40, 80)
CEILING_COLOR = (182, 255, 254)
PLAYER_COLOR = (255, 50, 50)
EXIT_COLOR = (50, 255, 50)
TEXT_COLOR = (255, 255, 255)

# Game constants
FOV = math.pi / 3  # 60 degrees field of view
HALF_FOV = FOV / 2
NUM_RAYS = 100
MAX_DEPTH = 10
MOVE_SPEED = 0.05
ROTATION_SPEED = 0.03
TEXTURE_SIZE = 512

# Generate maze using recursive backtracking
def generate_maze(width, height, extra_passage_prob=0.12):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    visited = [[False for _ in range(width)] for _ in range(height)]
    
    # Start from top-left corner
    stack = [(1, 1)]
    visited[1][1] = True
    maze[1][1] = 0
    
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    
    while stack:
        x, y = stack[-1]
        neighbors = []
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and not visited[ny][nx]:
                neighbors.append((nx, ny, dx, dy))
        
        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[y + dy//2][x + dx//2] = 0
            visited[ny][nx] = True
            stack.append((nx, ny))
        else:
            stack.pop()
    
    # Ensure there's an exit
    maze[height-2][width-2] = 0
    # Post-process: randomly remove some interior walls to increase passages
    for y in range(1, height-1):
        for x in range(1, width-1):
            if maze[y][x] == 1:
                # Count adjacent open cells
                open_neighbors = 0
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    if maze[y+dy][x+dx] == 0:
                        open_neighbors += 1
                # Remove wall with probability if it touches at least one open cell
                if open_neighbors >= 1 and random.random() < extra_passage_prob:
                    maze[y][x] = 0

    # Ensure exit stays open
    maze[height-2][width-2] = 0
    return maze

# Create textures
def create_wall_texture():
    texture = pygame.Surface((TEXTURE_SIZE, TEXTURE_SIZE))
    texture.fill(WALL_COLOR)
    
    # Add some pattern to the wall
    for i in range(0, TEXTURE_SIZE, 8):
        pygame.draw.line(texture, (80, 80, 120), (i, 0), (i, TEXTURE_SIZE), 1)
        pygame.draw.line(texture, (80, 80, 120), (0, i), (TEXTURE_SIZE, i), 1)
    
    # Add some random spots
    for _ in range(50):
        x = random.randint(0, TEXTURE_SIZE-1)
        y = random.randint(0, TEXTURE_SIZE-1)
        size = random.randint(1, 3)
        pygame.draw.circle(texture, (70, 70, 100), (x, y), size)
    
    return texture

def create_floor_texture():
    texture = pygame.Surface((TEXTURE_SIZE, TEXTURE_SIZE))
    texture.fill(FLOOR_COLOR)
    
    # Add grid pattern
    for i in range(0, TEXTURE_SIZE, 16):
        pygame.draw.line(texture, (30, 30, 60), (i, 0), (i, TEXTURE_SIZE), 1)
        pygame.draw.line(texture, (30, 30, 60), (0, i), (TEXTURE_SIZE, i), 1)
    
    return texture

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.move_speed = MOVE_SPEED
        self.rotation_speed = ROTATION_SPEED
        # Trail of positions (for monsters to follow)
        self.trail = deque(maxlen=2000)
    
    def rotate(self, direction):
        self.angle += direction * self.rotation_speed
        # Keep angle in [0, 2*pi)
        self.angle %= 2 * math.pi
    
    def move(self, direction, maze):
        # Calculate new position based on direction
        new_x = self.x + direction[0] * self.move_speed
        new_y = self.y + direction[1] * self.move_speed
        
        # Check for collisions with walls
        grid_x = int(new_x)
        grid_y = int(new_y)
        
        if 0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze):
            if maze[grid_y][grid_x] == 0:
                self.x = new_x
                self.y = new_y
        
        # Check diagonal movement
        grid_x = int(self.x)
        grid_y = int(new_y)
        if 0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze):
            if maze[grid_y][grid_x] == 0:
                self.y = new_y
                
        grid_x = int(new_x)
        grid_y = int(self.y)
        if 0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze):
            if maze[grid_y][grid_x] == 0:
                self.x = new_x


# Enemy class: simple 3D billboard-like rendering in the raycast view
class Enemy:
    def __init__(self, x, y):
        # Position in world coordinates (grid-based, use center of cell)
        self.x = x
        self.y = y
        # Animation state: 'idle', 'swing', 'slash', 'defend'
        self.state = 'idle'
        self.state_timer = 0.0
        # Sword angle in screen-space (radians) for simple 2D rendering
        self.sword_angle = -0.6

    def swing(self):
        self.state = 'swing'
        self.state_timer = 0.5
        # Play swing sound if available
        if SOUND_ENABLED and 'swing_sound' in globals() and swing_sound:
            try:
                swing_sound.play()
            except Exception:
                pass

    def slash(self):
        self.state = 'slash'
        self.state_timer = 0.4
        # Play slash sound if available
        if SOUND_ENABLED and 'slash_sound' in globals() and slash_sound:
            try:
                slash_sound.play()
            except Exception:
                pass

    def defend(self):
        self.state = 'defend'
        self.state_timer = 0.6
        # Play defend sound if available
        if SOUND_ENABLED and 'defend_sound' in globals() and defend_sound:
            try:
                defend_sound.play()
            except Exception:
                pass

    def update(self, dt, player):
        # Compute distance & facing relative to player
        dx = self.x - player.x
        dy = self.y - player.y
        dist = math.hypot(dx, dy)
        angle_to_player = math.atan2(dy, dx)
        angle_diff = (angle_to_player - player.angle + math.pi) % (2 * math.pi) - math.pi

        # Auto-attack when near the player and roughly facing them
        attack_range = 1.5
        facing_threshold = math.pi / 3.0
        if self.state == 'idle' and dist < attack_range and abs(angle_diff) < facing_threshold:
            self.swing()

        # Update timer and animate sword angle based on state
        if self.state_timer > 0:
            self.state_timer -= dt
            prog_total = 0.5 if self.state == 'swing' else (0.4 if self.state == 'slash' else 0.6)
            prog_total = max(prog_total, 0.001)
            progress = 1.0 - max(0.0, self.state_timer) / prog_total

            if self.state == 'swing':
                self.sword_angle = -0.7 + progress * 1.4
            elif self.state == 'slash':
                self.sword_angle = -0.4 + progress * 1.8
            elif self.state == 'defend':
                # Raise sword to block position and wobble a bit
                self.sword_angle = -1.2 + math.sin(progress * math.pi) * 0.25

            if self.state_timer <= 0:
                self.state = 'idle'
        else:
            # Idle breathing/wobble
            t = pygame.time.get_ticks() / 1000.0
            self.sword_angle = -0.6 + math.sin(t * 2.0) * 0.08

    def draw_3d(self, screen, player, rays):
        # Compute relative vector from player to enemy
        dx = self.x - player.x
        dy = self.y - player.y
        dist = math.hypot(dx, dy)

        # Angle to enemy
        angle = math.atan2(dy, dx)
        angle_diff = (angle - player.angle + math.pi) % (2 * math.pi) - math.pi

        # Only draw if in field of view and in front
        if abs(angle_diff) > HALF_FOV:
            return

        # Corrected projected distance (remove fish-eye)
        proj_dist = dist * math.cos(angle_diff)
        if proj_dist <= 0:
            return

        # Screen X position
        screen_x = (angle_diff / FOV + 0.5) * WIDTH

        # Occlusion: find nearest wall ray at that screen column
        ray_width = WIDTH / NUM_RAYS
        ray_idx = int(screen_x // ray_width)
        if 0 <= ray_idx < len(rays):
            wall_dist = rays[ray_idx]['dist']
            # If wall is closer than enemy, don't draw (occluded)
            if wall_dist < proj_dist - 0.05:
                return

        # Sprite scale: use projection similar to walls
        sprite_scale = 0.5
        size = min(HEIGHT, HEIGHT / (proj_dist + 0.0001)) * sprite_scale

        # Create a temporary surface for the enemy sprite (with per-pixel alpha)
        sprite_w = max(8, int(size * 0.6))
        sprite_h = max(16, int(size))
        sprite = pygame.Surface((sprite_w, sprite_h), pygame.SRCALPHA)

        # Body: vertical gradient rectangle (black center, slightly lighter sides)
        body_w = int(sprite_w * 0.6)
        body_h = int(sprite_h * 0.6)
        body_x = (sprite_w - body_w) // 2
        body_y = int(sprite_h * 0.28)
        for i in range(body_w):
            shade = 20 + int(150 * (1 - abs((i - body_w/2) / (body_w/2))))
            col = (0, 0, 0 + 0)
            pygame.draw.line(sprite, (0, 0, 0), (body_x + i, body_y), (body_x + i, body_y + body_h))

        # Head (red)
        head_r = max(2, int(sprite_h * 0.12))
        head_cx = sprite_w // 2
        head_cy = max(4, int(body_y - head_r))
        pygame.draw.circle(sprite, (255, 0, 0), (head_cx, head_cy), head_r)

        # Hand (red) on right side
        hand_r = max(2, int(head_r * 0.6))
        hand_x = int(sprite_w * 0.78)
        hand_y = int(body_y + body_h * 0.5)
        pygame.draw.circle(sprite, (255, 0, 0), (hand_x, hand_y), hand_r)

        # Sword (black blade) with red hilt on the sprite surface
        blade_len = sprite_h * 0.9
        sx = hand_x
        sy = hand_y
        ex = sx + math.cos(self.sword_angle) * blade_len
        ey = sy + math.sin(self.sword_angle) * blade_len
        blade_w = max(1, int(sprite_h * 0.04))
        pygame.draw.line(sprite, (0, 0, 0), (int(sx), int(sy)), (int(ex), int(ey)), blade_w)
        # Hilt
        hilt_x = sx + math.cos(self.sword_angle) * (sprite_h * 0.08)
        hilt_y = sy + math.sin(self.sword_angle) * (sprite_h * 0.08)
        pygame.draw.circle(sprite, (255, 0, 0), (int(hilt_x), int(hilt_y)), max(1, int(sprite_h * 0.04)))

        # Add simple shading based on angle_diff (turning left/right)
        shade_offset = int((angle_diff / HALF_FOV) * 50)
        overlay = pygame.Surface((sprite_w, sprite_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        if shade_offset > 0:
            pygame.draw.rect(overlay, (0, 0, 0, min(120, shade_offset)), (0, 0, sprite_w//2, sprite_h))
        else:
            pygame.draw.rect(overlay, (0, 0, 0, min(120, -shade_offset)), (sprite_w//2, 0, sprite_w//2, sprite_h))
        sprite.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        # Draw the sprite onto the screen centered at screen_x
        draw_x = int(screen_x - sprite_w / 2)
        draw_y = int((HEIGHT - size) / 2)
        screen.blit(sprite, (draw_x, draw_y))


# Monster that chases the player once it sees them and jumpscares on contact
class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.chasing = False
        # Make the monster faster and "super sensitive"
        self.speed = 0.12
        # Very large vision range and effectively full FOV so it detects the
        # player more easily (super sensitive)
        self.vision_range = 20.0
        self.vision_fov = math.pi * 2.0

    def can_see_player(self, player, maze):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        # Super sensitive: detect the player anywhere within vision_range
        # regardless of walls (very aggressive behavior)
        return dist <= self.vision_range

    def update(self, dt, player, maze):
        # If not yet chasing, check vision
        if not self.chasing and self.can_see_player(player, maze):
            self.chasing = True

        # If chasing, move towards player ignoring LOS
        if self.chasing:
            # Follow the exact path the player took (player.trail).
            # If a trail exists, target the oldest recorded position so the
            # monster follows the same path. Otherwise, fall back to direct chase.
            if hasattr(player, 'trail') and len(player.trail) > 0:
                target_x, target_y = player.trail[0]
                dx = target_x - self.x
                dy = target_y - self.y
                dist = math.hypot(dx, dy)
                # When close to this trail point, consume it so the monster
                # progresses along the path.
                if dist < 0.25:
                    try:
                        player.trail.popleft()
                    except Exception:
                        pass
                if dist <= 0.001:
                    return False
                nx = dx / dist
                ny = dy / dist
            else:
                dx = player.x - self.x
                dy = player.y - self.y
                dist = math.hypot(dx, dy)
                if dist <= 0.001:
                    return False
                nx = dx / dist
                ny = dy / dist

            # Attempt move with simple collision like player
            new_x = self.x + nx * self.speed
            new_y = self.y + ny * self.speed

            grid_x = int(new_x)
            grid_y = int(new_y)
            if 0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze) and maze[grid_y][grid_x] == 0:
                self.x = new_x
                self.y = new_y
            else:
                # try sliding on axes
                grid_x = int(self.x)
                grid_y = int(new_y)
                if 0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze) and maze[grid_y][grid_x] == 0:
                    self.y = new_y
                grid_x = int(new_x)
                grid_y = int(self.y)
                if 0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze) and maze[grid_y][grid_x] == 0:
                    self.x = new_x

            # If close enough to player, trigger jumpscare
            if math.hypot(player.x - self.x, player.y - self.y) < 1.0:
                # Play jumpscare sound if available
                if SOUND_ENABLED and 'jumpscare_sound' in globals() and jumpscare_sound:
                    try:
                        jumpscare_sound.play()
                    except Exception:
                        pass
                return True

        return False

    def draw_3d(self, screen, player, rays):
        # Simple billboard bright red blob (more vivid)
        dx = self.x - player.x
        dy = self.y - player.y
        dist = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)
        angle_diff = (angle - player.angle + math.pi) % (2 * math.pi) - math.pi
        if abs(angle_diff) > HALF_FOV:
            return
        proj_dist = dist * math.cos(angle_diff)
        if proj_dist <= 0:
            return
        screen_x = (angle_diff / FOV + 0.5) * WIDTH
        ray_width = WIDTH / NUM_RAYS
        ray_idx = int(screen_x // ray_width)
        if 0 <= ray_idx < len(rays):
            wall_dist = rays[ray_idx]['dist']
            if wall_dist < proj_dist - 0.05:
                return
        sprite_scale = 0.9
        size = min(HEIGHT, HEIGHT / (proj_dist + 0.0001)) * sprite_scale
        sprite_w = max(12, int(size * 0.6))
        sprite_h = max(24, int(size))
        sprite = pygame.Surface((sprite_w, sprite_h), pygame.SRCALPHA)
        # body: bright red for "make him red"
        pygame.draw.ellipse(sprite, (255, 0, 0), (0, 0, sprite_w, sprite_h))
        # eyes (bigger to be more expressive)
        eye_r = max(3, sprite_w//8)
        pygame.draw.circle(sprite, (255, 255, 255), (sprite_w//3, sprite_h//3), eye_r)
        pygame.draw.circle(sprite, (255, 255, 255), (2*sprite_w//3, sprite_h//3), eye_r)
        # pupils
        pupil_r = max(1, sprite_w//12)
        pygame.draw.circle(sprite, (0, 0, 0), (sprite_w//3, sprite_h//3), pupil_r)
        pygame.draw.circle(sprite, (0, 0, 0), (2*sprite_w//3, sprite_h//3), pupil_r)
        draw_x = int(screen_x - sprite_w / 2)
        draw_y = int((HEIGHT - size) / 2)
        screen.blit(sprite, (draw_x, draw_y))


# Raycasting engine
def cast_rays(player, maze, wall_texture, floor_texture):
    rays = []
    ray_angle = player.angle - HALF_FOV
    
    for ray in range(NUM_RAYS):
        # Cast ray
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)
        
        # Vertical intersection check
        v_x, v_y, v_dist = float('inf'), float('inf'), float('inf')
        depth = 0
        while depth < MAX_DEPTH:
            v_x = player.x + depth * cos_a
            v_y = player.y + depth * sin_a
            grid_x = int(v_x)
            grid_y = int(v_y)
            
            if 0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze):
                if maze[grid_y][grid_x] == 1:
                    v_dist = depth
                    break
            depth += 0.1
        
        # Horizontal intersection check
        h_x, h_y, h_dist = float('inf'), float('inf'), float('inf')
        depth = 0
        while depth < MAX_DEPTH:
            h_x = player.x + depth * cos_a
            h_y = player.y + depth * sin_a
            grid_x = int(h_x)
            grid_y = int(h_y)
            
            if 0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze):
                if maze[grid_y][grid_x] == 1:
                    h_dist = depth
                    break
            depth += 0.1
        
        # Choose closer intersection
        if v_dist < h_dist:
            dist = v_dist
            wall_x = v_x
        else:
            dist = h_dist
            wall_x = h_x
        
        # Apply fish-eye correction
        dist *= math.cos(player.angle - ray_angle)
        
        # Calculate wall height
        wall_height = min(HEIGHT, HEIGHT / (dist + 0.0001))
        
        # Calculate texture coordinate
        tex_x = int((wall_x - int(wall_x)) * TEXTURE_SIZE) % TEXTURE_SIZE
        if v_dist < h_dist:
            tex_x = TEXTURE_SIZE - tex_x - 1
        
        # Store ray info
        rays.append({
            'dist': dist,
            'height': wall_height,
            'tex_x': tex_x
        })
        
        ray_angle += FOV / NUM_RAYS
    
    return rays

# Draw game
def draw_game(screen, rays, wall_texture, floor_texture, player, maze, exit_pos):
    # Draw ceiling
    pygame.draw.rect(screen, CEILING_COLOR, (0, 0, WIDTH, HEIGHT // 2))
    
    # Draw floor
    pygame.draw.rect(screen, FLOOR_COLOR, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    
    # Draw walls
    ray_width = WIDTH / NUM_RAYS
    for i, ray in enumerate(rays):
        if ray['dist'] < MAX_DEPTH:
            # Get texture strip
            tex_x = ray['tex_x']
            wall_strip = wall_texture.subsurface(tex_x, 0, 1, TEXTURE_SIZE)
            
            # Scale texture to wall height
            wall_height = min(ray['height'], HEIGHT)
            scaled_strip = pygame.transform.scale(wall_strip, (int(ray_width), int(wall_height)))
            
            # Draw wall strip
            screen.blit(scaled_strip, (i * ray_width, (HEIGHT - wall_height) // 2))
    
    # Draw exit marker
    exit_x, exit_y = exit_pos
    dist_to_exit = math.sqrt((player.x - exit_x) ** 2 + (player.y - exit_y) ** 2)
    if dist_to_exit < 1.5:
        # Draw exit as a green column
        exit_angle = math.atan2(exit_y - player.y, exit_x - player.x)
        angle_diff = (exit_angle - player.angle + math.pi) % (2 * math.pi) - math.pi
        if abs(angle_diff) < HALF_FOV:
            # Calculate screen position
            screen_x = (angle_diff / FOV + 0.5) * WIDTH
            exit_dist = max(0.1, dist_to_exit)
            exit_height = min(HEIGHT, HEIGHT / exit_dist)
            pygame.draw.rect(screen, EXIT_COLOR, (screen_x - 10, (HEIGHT - exit_height) // 2, 20, exit_height))
    
    # Draw player position on minimap
    draw_minimap(screen, player, maze, exit_pos)

# Draw minimap
def draw_minimap(screen, player, maze, exit_pos):
    # Make minimap larger and adaptive to screen width (capped)
    map_size = int(min(400, WIDTH * 0.25))
    map_surface = pygame.Surface((map_size, map_size))
    map_surface.set_alpha(200)
    
    # Draw maze on minimap
    cell_size = map_size / len(maze)
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 1:
                pygame.draw.rect(map_surface, (80, 80, 120), (x * cell_size, y * cell_size, cell_size, cell_size))
    
    # Draw exit
    exit_x, exit_y = exit_pos
    pygame.draw.rect(map_surface, EXIT_COLOR, (exit_x * cell_size, exit_y * cell_size, cell_size, cell_size))
    
    # Draw player
    player_x = player.x * cell_size
    player_y = player.y * cell_size
    pygame.draw.circle(map_surface, PLAYER_COLOR, (player_x, player_y), cell_size / 2)
    
    # Draw player direction
    end_x = player_x + math.cos(player.angle) * cell_size
    end_y = player_y + math.sin(player.angle) * cell_size
    pygame.draw.line(map_surface, (255, 255, 255), (player_x, player_y), (end_x, end_y), 2)
    
    screen.blit(map_surface, (WIDTH - map_size - 10, 10))

# Draw UI
def draw_ui(screen, game_state):
    if game_state == "start":
        title_font = pygame.font.SysFont(None, 64)
        text_font = pygame.font.SysFont(None, 32)
        
        title = title_font.render("3D MAZE ESCAPE", True, TEXT_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        
        start_text = text_font.render("Press SPACE to start", True, TEXT_COLOR)
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
        
        controls = [
            "WASD - Move",
            "Arrow Keys - Look",
            "Find the green exit!"
        ]
        
        for i, line in enumerate(controls):
            text = text_font.render(line, True, TEXT_COLOR)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 60 + i*30))
            
    elif game_state == "win":
        title_font = pygame.font.SysFont(None, 64)
        text_font = pygame.font.SysFont(None, 32)
        
        title = title_font.render("YOU ESCAPED!", True, EXIT_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        
        restart = text_font.render("Press SPACE to play again", True, TEXT_COLOR)
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2))

# Main game function
def main():
    # Generate maze
    maze_width, maze_height = 21, 21
    maze = generate_maze(maze_width, maze_height)
    exit_pos = (maze_width - 2, maze_height - 2)
    
    # Create player at start position
    player = Player(1.5, 1.5)
    
    # Create textures
    wall_texture = create_wall_texture()
    floor_texture = create_floor_texture()

    # Enemies disabled per user request
    enemies = []
    
    # Game state
    game_state = "start"  # "start", "playing", "win"
    
    # Main game loop
    running = True
    while running:
        # Cap frame rate and get delta time
        dt = clock.tick(60) / 1000.0

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_state == "start":
                        game_state = "playing"
                        if SOUND_ENABLED and 'start_sound' in globals() and start_sound:
                            try:
                                start_sound.play()
                            except Exception:
                                pass
                    elif game_state == "win":
                        # Reset game
                        maze = generate_maze(maze_width, maze_height)
                        exit_pos = (maze_width - 2, maze_height - 2)
                        player = Player(1.5, 1.5)
                        # Keep enemies disabled on reset
                        enemies = []
                        game_state = "playing"
                        if SOUND_ENABLED and 'start_sound' in globals() and start_sound:
                            try:
                                start_sound.play()
                            except Exception:
                                pass

        keys = pygame.key.get_pressed()

        if game_state == "playing":
            # Handle player movement
            move_dir = [0, 0]
            if keys[pygame.K_w]:
                move_dir[0] += math.cos(player.angle)
                move_dir[1] += math.sin(player.angle)
            if keys[pygame.K_s]:
                move_dir[0] -= math.cos(player.angle)
                move_dir[1] -= math.sin(player.angle)
            if keys[pygame.K_a]:
                move_dir[0] += math.cos(player.angle - math.pi/2)
                move_dir[1] += math.sin(player.angle - math.pi/2)
            if keys[pygame.K_d]:
                move_dir[0] += math.cos(player.angle + math.pi/2)
                move_dir[1] += math.sin(player.angle + math.pi/2)

            # Normalize movement
            if move_dir[0] != 0 or move_dir[1] != 0:
                length = math.sqrt(move_dir[0]**2 + move_dir[1]**2)
                move_dir[0] /= length
                move_dir[1] /= length
                player.move(move_dir, maze)

            # Handle rotation
            if keys[pygame.K_LEFT]:
                player.rotate(-1)
            if keys[pygame.K_RIGHT]:
                player.rotate(1)

            # Quick debug/test controls for enemy actions (J=Swing, K=Slash, L=Defend)
            if enemies:
                if keys[pygame.K_j]:
                    enemies[0].swing()
                if keys[pygame.K_k]:
                    enemies[0].slash()
                if keys[pygame.K_l]:
                    enemies[0].defend()

            # Update enemies
            for e in enemies:
                e.update(dt, player)

            # Check win condition
            dist_to_exit = math.sqrt((player.x - exit_pos[0])**2 + (player.y - exit_pos[1])**2)
            if dist_to_exit < 0.8:
                game_state = "win"
                if SOUND_ENABLED and 'win_sound' in globals() and win_sound:
                    try:
                        win_sound.play()
                    except Exception:
                        pass

            # Cast rays
            rays = cast_rays(player, maze, wall_texture, floor_texture)

            # Draw everything
            screen.fill(BACKGROUND)
            draw_game(screen, rays, wall_texture, floor_texture, player, maze, exit_pos)

            # Draw enemies after world so they appear on top (pass rays for occlusion)
            for e in enemies:
                e.draw_3d(screen, player, rays)
        else:
            screen.fill(BACKGROUND)
            draw_ui(screen, game_state)

        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
