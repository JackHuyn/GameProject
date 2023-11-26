import pygame
from settings import *
from entity import Entity
from support import *
from random import *

class Enemy(Entity):
	def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp):

		# general setup
		super().__init__(groups)
		self.sprite_type = 'enemy'

		# graphics setup
		self.import_graphics(monster_name)
		self.status = 'down'
		self.image = self.animations[self.status][self.frame_index]

		# movement
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-10)
		self.obstacle_sprites = obstacle_sprites

		# stats
		self.monster_name = monster_name
		monster_info = monster_data[self.monster_name]
		self.health = monster_info['health']
		self.exp = monster_info['exp']
		self.speed = monster_info['speed']
		self.attack_damage = monster_info['damage']
		self.resistance = monster_info['resistance']
		self.attack_radius = monster_info['attack_radius']
		self.notice_radius = monster_info['notice_radius']
		self.attack_type = monster_info['attack_type']
		# self.attack_cooldown = monster_info['attack cooldown']

		# player interaction
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
		self.damage_player = damage_player
		self.trigger_death_particles = trigger_death_particles
		self.add_exp = add_exp

		# invincibility timer
		self.vulnerable = True
		self.hit_time = None
		self.invincibility_duration = 300

		# sounds
		self.death_sound = pygame.mixer.Sound('../audio/death.wav')
		self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
		self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
		self.death_sound.set_volume(0)
		self.hit_sound.set_volume(0)
		self.attack_sound.set_volume(0)

		# Roaming state variables
		self.roaming_timer = 0
		self.roaming_duration = 2 * 1000  # Total duration for each roaming cycle (in milliseconds)
		self.roaming_status = False
		self.original_pos = pos  # Save the original position for returning
		self.roaming_speed = 1

		self.idle_timer = 0
		self.idle_duration = 10* 1000



	def import_graphics(self,name):
			monster_path = f'../graphics/monsters/{name}/'
			self.animations = {'up': [],'down': [],'left': [],'right': [],
				'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
				'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

			for animation in self.animations.keys():
				full_path = monster_path + animation
				self.animations[animation] = import_folder(full_path)
				

	def get_player_distance_direction(self,player):
		enemy_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(player.rect.center)
		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance,direction)

	def get_status(self, player):
		distance, direction = self.get_player_distance_direction(player)
		if distance <= self.attack_radius:
			if self.can_attack:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle', '_attack')
				elif not 'attack' in self.status:
					self.status += '_attack'
			elif 'attack' in self.status:
				self.status = self.status.replace('_attack', '')
		elif distance <= self.notice_radius:

			if direction.x < 0 and abs(direction.x) > abs(direction.y):
				self.status = 'left'
			elif direction.x > 0 and abs(direction.x) > abs(direction.y):
				self.status = 'right'
			elif direction.y < 0 and abs(direction.y) >= abs(direction.x):
				self.status = 'up'
			else:
				self.status = 'down'
		else:
			if not 'idle' in self.status:
				self.status += '_idle'
			

	def actions(self,player):
		if 'attack' in self.status:
			self.attack_time = pygame.time.get_ticks()
			self.damage_player(self.attack_damage,self.attack_type)
			self.attack_sound.play()
		elif not 'idle' in self.status and not 'attack' in self.status:
			self.direction = self.get_player_distance_direction(player)[1]
		# elif 'idle' in self.status and not self.roaming_status:
		# 	self.direction = pygame.math.Vector2()

	def animate(self):
		animation = self.animations[self.status]
		
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if 'attack' in self.status:
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True

		if not self.vulnerable:
			if current_time - self.hit_time >= self.invincibility_duration:
				self.vulnerable = True

	def get_damage(self,player,attack_type):
		if self.vulnerable:
			self.hit_sound.play()
			self.direction = self.get_player_distance_direction(player)[1]
			if attack_type == 'weapon':
				self.health -= player.get_full_weapon_damage()
			else:
				self.health -= player.get_full_magic_damage()
			self.hit_time = pygame.time.get_ticks()
			self.vulnerable = False

	def check_death(self):
		if self.health <= 0:
			self.kill()
			self.trigger_death_particles(self.rect.center,self.monster_name)
			self.add_exp(self.exp)
			self.death_sound.play()

	def hit_reaction(self):
		if not self.vulnerable:
			self.direction *= -self.resistance

	def roam_around(self):
		# Check if it's time to change roaming direction
		current_time = pygame.time.get_ticks()

		if (current_time - self.roaming_timer >= self.roaming_duration):
			self.roaming_status = True
			self.roaming2()
			self.roaming_timer = current_time
		

			

		
	def roaming(self):

		# Generate random x and y values for the new direction
		random_x = randint(-1, 1)
		random_y = randint(-1, 1)

		# Limit the enemy's roaming range
		random_x = max(-1, min(1, random_x))
		random_y = max(-1, min(1, random_y))

		# Set the new direction
		self.direction.x = random_x
		self.direction.y = random_y

		# Check if the direction vector has a non-zero length
		if self.direction.length() > 0:
			# Normalize the direction vector
			self.direction.normalize()

			# Adjust the distance the enemy will move
			max_range = TILESIZE   # Change this value according to your needs
			
			# Update the enemy's position
			new_x = max(self.rect.x - max_range, min(self.rect.x + max_range, self.rect.x + int(self.direction.x * max_range)))
			new_y = max(self.rect.y - max_range, min(self.rect.y + max_range, self.rect.y + int(self.direction.y * max_range)))
			# Check if the new position is within the screen boundaries
			screen_rect = pygame.display.get_surface().get_rect()
			if screen_rect.collidepoint(new_x, new_y):
				self.rect.topleft = (new_x, new_y)

			self.roaming_status = False
		

	def roaming2(self):

		# If it's been less than 2 seconds since the last roaming, do nothing
		random_x = randint(-1, 1)
		random_y = randint(-1, 1)

		# Limit the enemy's roaming range
		random_x = max(-1, min(1, random_x))
		random_y = max(-1, min(1, random_y))

		# Set the new direction
		self.direction.x = random_x
		self.direction.y = random_y

		# Check if the direction vector has a non-zero length
		if self.direction.length() > 0:
			# Normalize the direction vector
			self.direction.normalize()

			distance_to_original = pygame.math.Vector2(self.original_pos) - pygame.math.Vector2(self.rect.topleft)
			if distance_to_original.length() > 5:
				# Check if inverting the direction would take the enemy closer to the original position
				modified_direction = pygame.math.Vector2(self.direction.x * distance_to_original.x, self.direction.y * distance_to_original.y)
				if modified_direction.length() < distance_to_original.length():
					# Set the direction to move towards the original position
					self.direction.x = distance_to_original.x
					self.direction.y = distance_to_original.y



			if self.direction.x < 0 and abs(self.direction.x) > abs(self.direction.y):
				self.status = 'left'
			elif self.direction.x > 0 and abs(self.direction.x) > abs(self.direction.y):
				self.status = 'right'
			elif self.direction.y < 0 and abs(self.direction.y) >= abs(self.direction.x):
				self.status = 'up'
			else:
				self.status = 'down'

			
			


	def invert_direction(self):
		# Invert the direction
		self.direction *= -1

			
	def update(self):
		self.hit_reaction()
		self.move(self.speed)
		self.animate()
		self.cooldowns()
		self.check_death()
		self.roam_around()

	def enemy_update(self,player):
		self.get_status(player)
		self.actions(player)
		