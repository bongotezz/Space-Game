# Enemies
import pygame
from os import path

class Enemy(pygame.sprite.Sprite):
    def __init__(self, bounds, startX, startY, shipType): # bounds is screen size
        pygame.sprite.Sprite.__init__(self)

        self.OffScreenY = startY * -1
        self.onScreen = False
        self.startx = startX
        self.starty = startY
        self.moveTimer = 200

        self.image = pygame.image.load( 'Images/enemy'+ shipType + '.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(50,41))
        self.rect = self.image.get_rect(center = (self.startx, self.OffScreenY)) # Gets the rectangle around the sprite
        self.score = int(shipType[len(shipType)-1]) * 10

    def moveOntoScreen(self):
        if not self.onScreen:
            self.rect.y += 5
            if self.rect.centery >= self.starty:
                self.onScreen = True

        

    def update(self, direction):
        self.moveOntoScreen()
        if self.moveTimer >= 0:
            self.moveTimer -= 1
        if self.onScreen and self.moveTimer <=0:
            self.rect.x += direction

class Bomber(pygame.sprite.Sprite):
    def __init__(self,WIDTH,side):
        pygame.sprite.Sprite.__init__(self)
        self.WIDTH = WIDTH
        self.side = side
        self.score = 1000
        self.payload = True
        self.image = pygame.image.load('Images/ufoRed.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(45,45))

        if self.side == 'left':
            self.rect = self.image.get_rect(topleft = (-100,70))
        else:
            self.rect = self.image.get_rect(topleft = (self.WIDTH + 100,70))


    def update(self):
        if self.side == 'left':
            self.rect.x += 2
        else:
            self.rect.x -= 2

        if self.rect.left >= self.WIDTH + 150 or self.rect.left <= -150:
            self.kill()