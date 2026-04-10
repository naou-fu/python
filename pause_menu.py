import pygame
import sys

class PauseMenu:
    def __init__(self, screen, WIDTH, HEIGHT, WHITE):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.WHITE = WHITE
        self.options = ["Resume", "Restart", "Quit"]
        self.selected = 0
        self.font = pygame.font.Font(None, 96)
        self.font2 = pygame.font.Font(None, 48)

    def show(self):
        while True:
            self.screen.fill(self.WHITE)
            text = self.font.render("PAUSED", True, (0, 0, 255))
            text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 80))
            self.screen.blit(text, text_rect)
            for i, option in enumerate(self.options):
                color = (0, 0, 0)
                bg = None
                if i == self.selected:
                    color = (255, 255, 255)
                    bg = (0, 100, 255)
                opt_text = self.font2.render(option, True, color, bg)
                opt_rect = opt_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + i * 60))
                self.screen.blit(opt_text, opt_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.selected = (self.selected - 1) % len(self.options)
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        self.selected = (self.selected + 1) % len(self.options)
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if self.options[self.selected] == "Resume":
                            return 'resume'
                        elif self.options[self.selected] == "Restart":
                            return 'restart'
                        elif self.options[self.selected] == "Quit":
                            pygame.quit()
                            sys.exit()
