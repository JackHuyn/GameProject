import pygame, sys
from settings import *
from level import Level
from frontpage import FrontPage
from characterSelections import CharacterSelection

class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

        self.level = Level()

        # Flags for game states
        self.in_front_page = True
        self.in_game = False
        self.in_character_selection = False
        self.game_running = True

        # Buttons
        self.front_page = FrontPage(self.screen)

    def run(self):
        while self.game_running:
            while self.in_front_page:
                self.front_page.draw()
                action = self.front_page.handle_events()
                if action == "start":
                    self.in_front_page = False
                    self.in_game = True
                    self.in_character_selection = True
                    self.character_selection = CharacterSelection(self.screen)
                elif action == "load":
                    self.level.player.kill()
                    self.level.load_game('011200')
                    self.in_front_page = False
                    self.in_game = True
                    self.level.run()
                elif action == "credit":
                    # Handle showing credits
                    pass

            while self.in_character_selection:
                self.character_selection.draw()
                action = self.character_selection.handle_events()
                if action == "select":
                    # Do something with the selected character, e.g., create the player with the selected character
                    # self.level.player.set_character(self.character_selection.selected_character)
                    self.in_game = True
                    self.in_character_selection = False

            while self.in_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.level.toggle_menu()
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_l:
                            self.level.save_game('011200', self.level.player)

                self.screen.fill(WATER_COLOR)
                self.level.run()
                pygame.display.update()
                self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()