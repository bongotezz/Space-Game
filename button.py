import pygame

class Button(pygame.sprite.Sprite):
	def __init__(self, bounds, active, pos, label):
		pygame.sprite.Sprite.__init__(self)

		self.bounds = bounds
		self.active = active
		self.pos = pos
		self.label = label
		self.font = pygame.font.Font('font/kenvector_future.ttf',20)
		self.image = pygame.image.load("Images/buttonRed.png").convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.activeImage = pygame.image.load("Images/buttonBlue.png").convert_alpha()
		self.inactiveImage = pygame.image.load("Images/buttonRed.png").convert_alpha()
		self.text = self.font.render(self.label, False, (0,0,0))
		self.textRect = self.text.get_rect(topleft = (self.pos[0] + 20, self.pos[1] + 10))
		self.clicked = False

	def addLabel(self, screen):
		screen.blit(self.text, self.textRect)

	def update(self):
		mousePos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mousePos):
			self.active = 'active'
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				#print(self.label)
		else:
			self.active = 'inactive'


		if self.active == 'active':
			self.image = self.activeImage
		else:
			self.image = self.inactiveImage



