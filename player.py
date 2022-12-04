# Player
import pygame
from os import path
from laser import *

class Player(pygame.sprite.Sprite):
    def __init__(self, bounds):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/PlayerShip.png").convert_alpha() #loads the sprite file
        self.image = pygame.transform.scale(self.image,(50,41)) # Scale image down
        self.rect = self.image.get_rect() #gets the rectangle around the sprite
        self.speed = 8
        self.direction = pygame.math.Vector2()
        self.bounds = bounds
        self.rect.centerx = self.bounds[0] / 2 #width
        self.rect.bottom = self.bounds[1] - (bounds[1] / 3) #height
        self.shoot_delay = 380 # delay in ticks for firing lasers -----------------------------------------------
        self.last_shot = pygame.time.get_ticks() # the last time a laser was fired----------------------------
        self.ready = True

        self.lasers = pygame.sprite.Group()

        self.laserSound = pygame.mixer.Sound('Sounds/laser.wav')
        self.laserSound.set_volume(0.05)
       
        
    def getInput(self):
        # Check for keyboard input
        keyPressed = pygame.key.get_pressed()
                
        if keyPressed[pygame.K_w]:
            self.direction.y = -1
        elif keyPressed[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keyPressed[pygame.K_d]:
            self.direction.x = 1
        elif keyPressed[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0        
            
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        # Constrain player
        if self.rect.right > self.bounds[0]:
            self.rect.right = self.bounds[0]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > self.bounds[1]:
            self.rect.bottom = self.bounds[1]
        if self.rect.top < self.bounds[1] - self.bounds[1] / 3:
            self.rect.top = self.bounds[1] - self.bounds[1] / 3

        if keyPressed[pygame.K_SPACE]: # firing code
            laser = self.fire("left")
            if laser != "":
                self.lasers.add(laser)
            laser2 = self.fire("right")
            if laser2 != "":
                self.lasers.add(laser2)
            self.ready = False

    def rechargeLaser(self):
        if not self.ready:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.last_shot >= self.shoot_delay:
                self.ready = True
            
       
            
    def fire(self, side):
        now = pygame.time.get_ticks() # gets the time now
        
        if now - self.last_shot > self.shoot_delay:
            self.laserSound.play()
            if side == "left":
                laser = Laser(self.bounds, True, self.rect.centerx - 15, self.rect.top + 20)
            elif side == "right":
                laser = Laser(self.bounds, True, self.rect.centerx + 15, self.rect.top + 20)
                self.last_shot = now
            return laser
        else:
            return ""

    def reset(self): # Sets position after death
        self.rect.centerx = self.bounds[0] / 2 #width
        self.rect.bottom = self.bounds[1] - (self.bounds[1] / 3) #height

    def update(self):
        self.getInput()
        self.rechargeLaser()
        