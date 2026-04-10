import pygame
import sys
import random
from pause_menu import PauseMenu
from powerup_dropper import PowerupDropper
from yellow_enemy import YellowEnemy
from powerup import Powerup
from game_platform import GamePlatform

def run_game(player, all_sprites, platforms, enemies, enemy_bullets, WIDTH, HEIGHT, screen, clock, WHITE, RED, max_health, Enemy, EnemyBullet):
    GAME_TIMER_MAX = 30
    game_timer_start = pygame.time.get_ticks()
    wave_timer_start = None
    in_wave_timer = False
    game_timer_countdown = GAME_TIMER_MAX
    score = 0
    player_health = max_health
    running = True
    game_over = False
    powerups = pygame.sprite.Group()
    wave_time = 5  # Initial wave time in seconds
    min_wave_time = 2  # Minimum allowed wave time
    wave_number = 1  # Track the current wave
    # Reset groups and player
    all_sprites.empty()
    platforms.empty()
    enemies.empty()
    enemy_bullets.empty()
    player.rect.topleft = (100, HEIGHT - 150)
    all_sprites.add(player)
    # Recreate platforms
    ground = GamePlatform(0, HEIGHT - 40, WIDTH, 40)
    platform1 = GamePlatform(200, HEIGHT - 200, 300, 20)
    platform2 = GamePlatform(600, HEIGHT - 350, 250, 20)
    platform3 = GamePlatform(1000, HEIGHT - 500, 300, 20)
    platform4 = GamePlatform(1500, HEIGHT - 250, 200, 20)
    platform5 = GamePlatform(400, HEIGHT - 600, 200, 20)
    platform6 = GamePlatform(900, HEIGHT - 150, 180, 20)
    platform7 = GamePlatform(1300, HEIGHT - 400, 220, 20)
    platform8 = GamePlatform(1700, HEIGHT - 600, 180, 20)
    platform9 = GamePlatform(100, HEIGHT - 300, 150, 20)
    platform10 = GamePlatform(800, HEIGHT - 700, 220, 20)
    platform11 = GamePlatform(1400, HEIGHT - 100, 160, 20)
    platform12 = GamePlatform(500, HEIGHT - 800, 200, 20)
    platforms.add(ground, platform1, platform2, platform3, platform4, platform5, platform6, platform7,
                   platform8, platform9, platform10, platform11, platform12)
    all_sprites.add(ground, platform1, platform2, platform3, platform4, platform5, platform6, platform7,
                    platform8, platform9, platform10, platform11, platform12)
    # Initial enemy spawn positions
    enemy_spawn_positions = [
        (600, HEIGHT - 80),
        (1200, HEIGHT - 300),
        (300, HEIGHT - 500),
        (1000, HEIGHT - 200)
    ]
    for pos in enemy_spawn_positions:
        e = Enemy(pos[0], pos[1], player, platforms, enemy_bullets, WIDTH)
        enemies.add(e)
        all_sprites.add(e)
    yellow_enemies_spawned = False
    enemy_respawn_timer = None
    yellow_enemies = pygame.sprite.Group()
    powerup_dropper = PowerupDropper(all_sprites, powerups)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = PauseMenu(screen, WIDTH, HEIGHT, WHITE)
                    menu_action = menu.show()
                    if menu_action == 'resume':
                        continue
                    elif menu_action == 'restart':
                        return
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_e:
                    player.shoot()

        player.update(platforms, WIDTH)
        enemies.update()
        enemy_bullets.update()
        yellow_enemies.update()
        powerups.update(platforms)

        # Bullet-enemy collision (2 hits for orange enemies)
        for bullet in player.bullets:
            hit_list = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in hit_list:
                if hasattr(enemy, 'take_hit'):
                    enemy.take_hit()
                bullet.kill()
                # Only score if enemy is killed
                if not enemy.alive():
                    score += 1
                    # Randomly drop powerup (30% chance)
                    if random.random() < 0.3:
                        powerup = Powerup(enemy.rect.centerx, enemy.rect.bottom)
                        powerups.add(powerup)
                        all_sprites.add(powerup)
        # Bullet-yellow enemy collision
        for bullet in player.bullets:
            hit_list = pygame.sprite.spritecollide(bullet, yellow_enemies, True)
            if hit_list:
                bullet.kill()
                score += len(hit_list)

        # Enemy respawn logic with 30-second global timer
        now = pygame.time.get_ticks()
        # Calculate game timer countdown
        if not in_wave_timer:
            elapsed = (now - game_timer_start) / 1000.0
            game_timer_countdown = max(0, int(GAME_TIMER_MAX - elapsed))
        # Start wave timer if either: no enemies OR game timer hits 0
        trigger_wave_timer = (len(enemies) == 0 or game_timer_countdown == 0)
        if trigger_wave_timer and not in_wave_timer:
            in_wave_timer = True
            wave_timer_start = now
        if in_wave_timer:
            wave_timer_elapsed = (now - wave_timer_start) / 1000.0 if wave_timer_start else 0
            if wave_timer_elapsed >= wave_time:
                # Spawn new wave
                current_enemy_count = len(enemy_spawn_positions) + 4
                if current_enemy_count > 64:
                    current_enemy_count = 64
                platform_list = list(platforms)
                spawn_platforms = [p for p in platform_list if p != ground]
                for _ in range(current_enemy_count):
                    plat = random.choice(spawn_platforms)
                    x = random.randint(plat.rect.left, plat.rect.right - 40)
                    y = plat.rect.top - 40
                    e = Enemy(x, y, player, platforms, enemy_bullets, WIDTH)
                    enemies.add(e)
                    all_sprites.add(e)
                # Drop powerups after respawn
                powerup_dropper.drop_powerups_on_wave(enemies)
                # Decrease wave_time for next wave, but not below minimum
                wave_time = max(min_wave_time, wave_time - 1)
                wave_number += 1
                # Reset timers
                game_timer_start = now
                wave_timer_start = None
                in_wave_timer = False
        else:
            # If not in wave timer, ensure wave_timer_start is None
            wave_timer_start = None

        # Spawn yellow enemies at score 20
        if not yellow_enemies_spawned and score >= 20:
            yellow_enemies_spawned = True
            platform_list = list(platforms)
            spawn_platforms = [p for p in platform_list if p != ground]
            for _ in range(4):
                plat = random.choice(spawn_platforms)
                x = random.randint(plat.rect.left, plat.rect.right - 40)
                y = plat.rect.top - 40
                ye = YellowEnemy(x, y, player, platforms, enemy_bullets, WIDTH)
                yellow_enemies.add(ye)
                all_sprites.add(ye)

        # Enemy bullet - player collision
        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            player_health -= 1
            if player_health <= 0:
                game_over = True
                running = False

        # Respawn player if falls off screen
        if player.rect.top > HEIGHT:
            player.rect.topleft = (100, HEIGHT - 150)
            player.vel_y = 0

        # Drawing
        screen.fill(WHITE)
        all_sprites.draw(screen)
        player.bullets.draw(screen)
        enemy_bullets.draw(screen)
        yellow_enemies.draw(screen)
        powerups.draw(screen)
        # Draw health bars for orange enemies
        for enemy in enemies:
            if hasattr(enemy, 'draw'):
                enemy.draw(screen)
        # Draw score and wave number
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0,0,0))
        screen.blit(score_text, (10, 10))
        wave_text = font.render(f"Wave: {wave_number}", True, (0,0,255))
        screen.blit(wave_text, (10, 50))

        # Draw game timer in the middle of the screen with 50% opacity
        # Show the game timer countdown or wave timer countdown
        timer_font = pygame.font.Font(None, 72)
        import math
        if in_wave_timer:
            wave_timer_elapsed = (now - wave_timer_start) / 1000.0 if wave_timer_start else 0
            timer_str = f"Wave in: {int(wave_time - wave_timer_elapsed)}s"
        else:
            timer_str = f"Game Timer: {game_timer_countdown}s"
        timer_text = timer_font.render(timer_str, True, (0,0,0))
        timer_surface = pygame.Surface(timer_text.get_size(), pygame.SRCALPHA)
        timer_surface.fill((255,255,255,0))
        timer_text.set_alpha(128)  # 50% opacity
        timer_surface.blit(timer_text, (0,0))
        timer_rect = timer_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(timer_surface, timer_rect)
        # Draw enemy respawn timer if waiting
        if len(enemies) == 0 and enemy_respawn_timer is not None:
            elapsed = (pygame.time.get_ticks() - enemy_respawn_timer) / 1000.0
            time_left = max(0, wave_time - int(elapsed))
            timer_text = font.render(f"Next wave in: {time_left}s", True, (255,0,0))
            timer_rect = timer_text.get_rect(midtop=(WIDTH // 2, 20))
            screen.blit(timer_text, timer_rect)
        # Draw health bar
        bar_width = 180
        bar_height = 25
        bar_x = 10
        bar_y = 50
        pygame.draw.rect(screen, (0,0,0), (bar_x-2, bar_y-2, bar_width+4, bar_height+4), 2)
        pygame.draw.rect(screen, (200,200,200), (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (player_health / max_health))
        pygame.draw.rect(screen, (255,0,0), (bar_x, bar_y, health_width, bar_height))
        health_percent = int((player_health / max_health) * 100)
        health_text = font.render(f"Health: {health_percent}%", True, (0,0,0))
        screen.blit(health_text, (bar_x + bar_width + 10, bar_y))
        pygame.display.flip()
        clock.tick(60)

    # Show Game Over screen if player lost
    if game_over:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 96)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text, text_rect)
        font2 = pygame.font.Font(None, 48)
        restart_text = font2.render("Press R to Restart or ESC to Quit", True, (0,0,0))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(restart_text, restart_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
