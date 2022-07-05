import pygame

class Shot(pygame.sprite.Sprite):
	def __init__(self,pos,speed,screen_height):
		super().__init__()
		self.image = pygame.Surface((5 ,25))
		self.image.fill((170, 0, 0))
		self.rect = self.image.get_rect(center = pos)
		self.speed = speed
		self.height_y_const = screen_height

	def hiting(self):
		if self.rect.y <= -50 or self.rect.y >= self.height_y_const + 50:
			self.kill()

	def update(self):
		self.rect.y += self.speed
		self.hiting()
