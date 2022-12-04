import pygame
from random import randint

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, bomb):
    	pygame.sprite.Sprite.__init__(self)

    	# Random int to determine the graphic to draw
    	self.smoke = randint(0,4)

    	self.timer = 10

    	if self.smoke == 0:
    		self.image = pygame.image.load('Images/smoke1.png').convert_alpha()    		
    	if self.smoke == 1:
    		self.image = pygame.image.load('Images/smoke2.png').convert_alpha()
    	if self.smoke == 2:
    		self.image = pygame.image.load('Images/smoke3.png').convert_alpha()
    	if self.smoke == 3:
    		self.image = pygame.image.load('Images/smoke4.png').convert_alpha()
    	if self.smoke == 4:
    		self.image = pygame.image.load('Images/smoke3.png').convert_alpha()

    	if bomb:
    		self.image = pygame.transform.scale(self.image,(252,300))
    	else:
    		self.image = pygame.transform.scale(self.image,(42,50))
    	self.rect = self.image.get_rect()
    	self.rect.centerx = x
    	self.rect.centery = y


    def update(self):
    	if self.timer <= 0:
    		self.kill()
    	self.timer -= 1
    	self.image = pygame.transform.rotate(self.image,3)
    	
