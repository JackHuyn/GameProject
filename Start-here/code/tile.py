import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		# might have to update the path
		self.image = pygame.image.load("Start-here/graphics/test/rock.png").convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)