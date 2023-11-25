import pygame
import sys
from settings import *

class CharacterSelection:
    def __init__(self, screen):
        self.screen = screen
        self.character_buttons = [
            pygame.Rect(50, HEIGHT // 2 - 25, 100, 50),
            pygame.Rect(WIDTH // 4 - 50, HEIGHT // 2 - 25, 100, 50),
            pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50),
            pygame.Rect(3 * WIDTH // 4 - 50, HEIGHT // 2 - 25, 100, 50),
            pygame.Rect(WIDTH - 150, HEIGHT // 2 - 25, 100, 50)
        ]
        self.selected_character = 0

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
                for i, button_rect in enumerate(self.character_buttons):
                    if button_rect.collidepoint(mouse_pos):
                        self.selected_character = i
                        return "select"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):  # Mouse wheel up or down
                if event.button == 4:  # Mouse wheel up
                    self.selected_character = (self.selected_character - 1) % 5
                elif event.button == 5:  # Mouse wheel down
                    self.selected_character = (self.selected_character + 1) % 5
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.selected_character = (self.selected_character - 1) % 5
                elif event.key == pygame.K_RIGHT:
                    self.selected_character = (self.selected_character + 1) % 5
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return "select"

        return None

    def draw(self):
        self.screen.fill(BLACK)
        for i, button_rect in enumerate(self.character_buttons):
            color = WHITE if i == self.selected_character else 'Gray'
            pygame.draw.rect(self.screen, color, button_rect)
            self.draw_text(f"Character {i+1}", 18, BLACK, *button_rect.center)
        pygame.display.update()
