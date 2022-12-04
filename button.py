import pygame

class Button(pygame.sprite.Sprite):
	def __init__(self, bounds, active):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load("Images/buttonRed.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.activeImage = pygame.image.load("Images/buttonBlue.png").convert_alpha()
		self.inactiveImage = pygame.image.load("Images/buttonRed.png").convert_alpha()
		self.bounds = bounds
		self.active = active

	def update(self):
		if self.active:
			self.image = self.activeImage
		else:
			self.image = self.inactiveImage

