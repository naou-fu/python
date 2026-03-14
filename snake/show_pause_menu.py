import pygame
import sys

def show_pause_menu(screen, WIDTH, HEIGHT, WHITE):
    options = ["Resume", "Restart", "Quit"]
    selected = 0
    font = pygame.font.Font(None, 96)
    font2 = pygame.font.Font(None, 48)
    while True:
        screen.fill(WHITE)
        text = font.render("PAUSED", True, (0, 0, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(text, text_rect)
        for i, option in enumerate(options):
            color = (0, 0, 0)
            bg = None
            if i == selected:
                color = (255, 255, 255)
                bg = (0, 100, 255)
            opt_text = font2.render(option, True, color, bg)
            opt_rect = opt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
            screen.blit(opt_text, opt_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(options)
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if options[selected] == "Resume":
                        return 'resume'
                    elif options[selected] == "Restart":
                        return 'restart'
                    elif options[selected] == "Quit":
                        pygame.quit()
                        sys.exit()
