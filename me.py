import pygame
from shooting import Shot

class Me(pygame.sprite.Sprite):
	def __init__(self,pos,const,speed):
		super().__init__()
		self.image = pygame.image.load('../space_invaders-main/pics/me.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom = pos)
		self.speed = speed
		self.max_x_const = const
		self.ready = True
		self.shot_time = 1
		self.shot_cooldown = 600

		self.shots = pygame.sprite.Group()

		self.shot_sound = pygame.mixer.Sound('../space_invaders-main/sound/shoot.wav')
		self.shot_sound.set_volume(0.5)

	def contoller(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.rect.x += self.speed
		elif keys[pygame.K_LEFT]:
			self.rect.x -= self.speed

		if keys[pygame.K_SPACE] and self.ready:
			self.shoot_bullet()
			self.ready = False
			self.shot_time = pygame.time.get_ticks()
			self.shot_sound.play()

	def reload(self):
		if not self.ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.shot_time >= self.shot_cooldown:
				self.ready = True

	def const(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.max_x_const:
			self.rect.right = self.max_x_const

	def shoot_bullet(self):
		self.shots.add(Shot(self.rect.center, -8, self.rect.bottom))

	def update(self):
		self.contoller()
		self.const()
		self.reload()
		self.shots.update()