import pygame
import sys
from settings import *

class FrontPage:
    def __init__(self, screen):
        self.screen = screen
        self.start_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 75, 100, 50)
        self.load_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
        self.credit_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 25, 100, 50)
        self.quit_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 75, 100, 50)

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if self.start_button_rect.collidepoint(mouse_pos):
                    return "start"
                elif self.load_button_rect.collidepoint(mouse_pos):
                    return "load"
                elif self.credit_button_rect.collidepoint(mouse_pos):
                    return "credit"
                elif self.quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        return None

    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.start_button_rect)
        pygame.draw.rect(self.screen, WHITE, self.load_button_rect)
        pygame.draw.rect(self.screen, WHITE, self.credit_button_rect)
        pygame.draw.rect(self.screen, WHITE, self.quit_button_rect)
        self.draw_text("Start", 24, BLACK, *self.start_button_rect.center)
        self.draw_text("Load", 24, BLACK, *self.load_button_rect.center)
        self.draw_text("Credit", 24, BLACK, *self.credit_button_rect.center)
        self.draw_text("Quit", 24, BLACK, *self.quit_button_rect.center)
        pygame.display.update()
