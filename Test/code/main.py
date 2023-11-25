import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()

		self.level = Level()

		# sound 
		# main_sound = pygame.mixer.Sound('../audio/main.ogg')
		# main_sound.set_volume(0.5)
		# main_sound.play(loops = -1)

		 # Flags for game states
		self.in_front_page = True
		self.in_game = False
		self.game_running = True

		# Buttons
		self.start_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 75, 100, 50)
		self.load_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
		self.credit_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 25, 100, 50)
		self.quit_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 75, 100, 50)


	def draw_text(self, text, size, color, x, y):
		font = pygame.font.Font(None, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect(center=(x, y))
		self.screen.blit(text_surface, text_rect)

	def front_page(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				mouse_pos = event.pos
				if self.start_button_rect.collidepoint(mouse_pos):
					self.in_front_page = False
					self.in_game = True
				elif self.load_button_rect.collidepoint(mouse_pos):
					# Handle loading saved game
					self.level.player.kill()
					self.level.load_game('011200')
					self.in_front_page = False
					self.in_game = True
					self.level.run()
				elif self.credit_button_rect.collidepoint(mouse_pos):
					# Handle showing credits
					pass
				elif self.quit_button_rect.collidepoint(mouse_pos):
					pygame.quit()
					sys.exit()

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


	def run(self):
		while self.in_front_page:
			self.front_page()

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
						self.level.save_game('011200',self.level.player)

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()