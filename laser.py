#player laser
import pygame
from os import path

class Laser(pygame.sprite.Sprite):
    def __init__(self, bounds, player, x, y): #bounds is screen size, player is booleen.
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        if self.player:
            self.image = pygame.image.load("Images/laserBlue13.png").convert_alpha() #loads the sprite file
        else:
            self.image = pygame.image.load("Images/laserRed14.png").convert_alpha() #loads the sprite file
        self.image = pygame.transform.scale(self.image,(5,28))
        self.rect = self.image.get_rect() #gets the rectangle around the sprite
        self.speedy = 0
        self.bounds = bounds
        self.rect.centerx = x
        self.rect.bottom = y
        
    def update(self):
        
        if self.player:
            self.speedy = -12
        else:
            self.speedy = 12
            
        self.rect.y += self.speedy
        
        if self.rect.bottom < -50 or self.rect.top > self.bounds[1] + 50:
            self.kill()
        
class Bomb(pygame.sprite.Sprite):
    def __init__(self, bounds, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/star3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.bounds = bounds
        self.speed = 15

    def update(self):
        self.rect.centery += self.speed

        if self.rect.top > self.bounds[1] - 50:
            self.kill()

