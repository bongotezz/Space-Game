import pygame, sys
from os import path
from player import *
from enemy import *
from random import choice, randint
from laser import *
from explosion import *

class Game:
    def __init__(self):
    	self.playerSprite = Player(bounds)
    	self.player = pygame.sprite.GroupSingle(self.playerSprite)

    	# Lives and score setup
    	self.lives = 3
    	self.score = 0
    	self.highScore = 0
    	self.respawnTime = 200 # Used for delay between death and reapawn
    	self.font = pygame.font.Font('font/kenvector_future.ttf',50)

    	# Enemy setup
    	self.enemies = pygame.sprite.Group()
    	self.enemyLasers = pygame.sprite.Group()
    	self.enemyDirection = 1
    	self.holdFire = True

    	self.bombers = pygame.sprite.Group()
    	self.bomberTimer = randint(400,800)
    	self.bombDropLocation = randint(50,WIDTH - 50)
    	self.bombDropped = False
    	self.bombs = pygame.sprite.Group()
    	self.bombExplosions = pygame.sprite.Group()

    	self.gameActive = False

    	# Music and sounds
    	music = pygame.mixer.Sound('Sounds/music.wav')
    	music.set_volume(0.02)
    	music.play(loops = -1)
    	self.laserSound = pygame.mixer.Sound('Sounds/laser.wav')
    	self.laserSound.set_volume(0.05)
    	self.explosionSound = pygame.mixer.Sound('Sounds/explosion.wav')
    	self.explosionSound.set_volume(0.05)

    	# Explosion setup
    	self.explosions = pygame.sprite.Group()



    def spawnEnemies(self):
    	enemyOffset = 83
    	enemyRows = 5
    	enemyColumns = 10
    	self.holdFire = False

    	while enemyRows > 0:
    		if enemyColumns <= 0: enemyColumns = 10
    		while enemyColumns > 0:
    			if enemyRows == 5:
    				ship = Enemy(bounds, 50 + (enemyOffset * (enemyColumns - 1)), 150 + (enemyOffset * (enemyRows - 1)), 'red1')
    				self.enemies.add(ship)
    			if enemyRows == 4:
    				ship = Enemy(bounds, 50 + (enemyOffset * (enemyColumns - 1)), 150 + (enemyOffset * (enemyRows - 1)), 'red2')
    				self.enemies.add(ship)
    			if enemyRows == 3:
    				ship = Enemy(bounds, 50 + (enemyOffset * (enemyColumns - 1)), 150 + (enemyOffset * (enemyRows - 1)), 'green3')
    				self.enemies.add(ship)
    			if enemyRows == 2:
    				ship = Enemy(bounds, 50 + (enemyOffset * (enemyColumns - 1)), 150 + (enemyOffset * (enemyRows - 1)), 'blue4')
    				self.enemies.add(ship)
    			if enemyRows == 1:
    				ship = Enemy(bounds, 50 + (enemyOffset * (enemyColumns - 1)), 150 + (enemyOffset * (enemyRows - 1)), 'black5')
    				self.enemies.add(ship)
    			enemyColumns -= 1
    		enemyRows -= 1

    def enemyMoveDirection(self, enemyDirection): # Keeps enemies on screen
    	allEnemies = self.enemies.sprites()
    	for enemy in allEnemies:
    		if enemy.rect.right >= WIDTH:
    			self.enemyDirection = -1
    		elif enemy.rect.left <= 0:
    			self.enemyDirection = 1

    def checkCollisions(self):
    	if self.player: # If the player exists
    		if self.player.sprite.lasers: # If player lasers exist
    			for laser in self.player.sprite.lasers:
    				enemiesHit = pygame.sprite.pygame.sprite.spritecollide(laser,self.enemies,True)
    				if enemiesHit:
    					for enemy in enemiesHit:
    						explosion = Explosion(enemy.rect.centerx,enemy.rect.centery,False)
    						self.explosions.add(explosion)
    						self.score += enemy.score
    						self.explosionSound.play()
    					laser.kill()

    				bombersHit = pygame.sprite.pygame.sprite.spritecollide(laser,self.bombers,True)
    				if bombersHit:
    					for bomber in bombersHit:
    						explosion = Explosion(bomber.rect.centerx,bomber.rect.centery, False)
    						self.explosions.add(explosion)
    						self.score += bomber.score
    						self.explosionSound.play()
    					laser.kill()

    	if self.enemyLasers and not self.holdFire:
    		for laser in self.enemyLasers:
    			if pygame.sprite.spritecollide(laser,self.player,False):
    				laser.kill()
    				self.endGame()
    				
    	if self.bombExplosions and not self.holdFire:
    		for explosion in self.bombExplosions:
    			if pygame.sprite.spritecollide(explosion,self.player,False):
    				explosion.kill()
    				self.endGame()
    				

    def endGame(self):
    	self.lives -= 1
    	print(self.lives)
    	self.holdFire = True

    	explosion = Explosion(self.playerSprite.rect.centerx,self.playerSprite.rect.centery,True)
    	self.explosions.add(explosion)
    	self.explosionSound.play()

    	if self.lives <= 0:
    		self.gameActive = False
    		self.enemyLasers.empty()
    		self.enemies.empty()
    		self.bombers.empty()
    		self.bombs.empty()
    		self.bombExplosions.empty()
    		self.playerSprite.lasers.empty()
    		self.explosions.empty()

    		if self.score > self.highScore:
    			self.highScore = self.score

    		self.score = 0

    def enemyShoot(self):
    	if self.enemies.sprites():
    		if not self.holdFire:
    			randomEnemy = choice(self.enemies.sprites())
    			laserSprite = Laser(bounds,False,randomEnemy.rect.centerx,randomEnemy.rect.centery)
    			self.enemyLasers.add(laserSprite)
    			self.laserSound.play()

    def respawnPlayer(self):
    	if not self.player:
    		self.player = pygame.sprite.GroupSingle(self.playerSprite)

    def spawnBomber(self):
    	self.bomberTimer -= 1
    	if self.bomberTimer <= 0:
    		side = choice(['left','right'])
    		bomber = Bomber(WIDTH,side)
    		self.bombers.add(bomber)
    		self.bombDropLocation = randint(50,WIDTH - 50)
    		self.bomberTimer = randint(800,1600)
    		self.bombDropped = False

    def checkBombDropLocation(self):
    	if self.bombers:
    		for bomber in self.bombers:
    			if bomber.rect.left <= self.bombDropLocation and bomber.rect.right >= self.bombDropLocation and self.bombDropped == False:
    				bomb = Bomb(bounds, bomber.rect.centerx,bomber.rect.centery)
    				self.bombs.add(bomb)
    				self.bombDropped = True

    def explodeBomb(self):
    	for bomb in self.bombs:
    		if bomb.rect.y >= HEIGHT - 200:
    			explosion = Explosion(bomb.rect.centerx,bomb.rect.centery, True)
    			self.bombExplosions.add(explosion)
    			self.explosionSound.play()

    def respawnTimer(self):
    	self.respawnTime -= 1
    	if self.respawnTime <= 0:
    		self.respawnTime = 200
    		self.holdFire = False
    		self.playerSprite.reset()
    		




    def run(self):
    	if self.gameActive:
    		if not self.enemies:
    			self.spawnEnemies()

    		if not self.holdFire:
    			self.player.update()
    		if self.player:
    			self.player.sprite.lasers.draw(screen) # Draws the player's lasers

    		self.enemyMoveDirection(self.enemyDirection)
    		self.player.sprite.lasers.update()
    		self.enemies.update(self.enemyDirection)
    		self.enemyLasers.update()
    		self.bombers.update()
    		self.bombs.update()
    		self.explosions.update()
    		self.bombExplosions.update()

    		self.spawnBomber()
    		self.checkBombDropLocation()
    		self.explodeBomb()
    	
    		if not self.holdFire:
    			self.player.draw(screen)

    		self.enemyLasers.draw(screen)
    		self.enemies.draw(screen)
    		self.explosions.draw(screen)
    		self.bombers.draw(screen)
    		self.bombs.draw(screen)
    		self.bombExplosions.draw(screen)

    		self.checkCollisions()

    		if self.holdFire:
    			self.respawnTimer()




if __name__ == '__main__':
	pygame.init()
	WIDTH = 900 # Screen width 900
	HEIGHT = 1080 # Screen height 1000
	bounds = [WIDTH, HEIGHT]
	screen = pygame.display.set_mode((bounds))
	clock = pygame.time.Clock()
	game = Game()
	gameName = game.font.render('Space Game', False, (255,255,255))
	gameNameRect = gameName.get_rect(center = (WIDTH / 2, HEIGHT / 3))
	directionsText1 = 'Space to shoot.'
	directionsText2 = 'WASD to move.'
	directionsText3 = 'Press P to play.'
	gameDirections = game.font.render(directionsText1, False, (255,255,255))
	gameDirectionsRect = gameDirections.get_rect(center = (WIDTH / 2, HEIGHT / 2))
	gameDirections2 = game.font.render(directionsText2, False, (255,255,255))
	gameDirectionsRect2 = gameDirections2.get_rect(center = (WIDTH / 2, HEIGHT / 2 - 50))
	gameDirections3 = game.font.render(directionsText3, False, (255,255,255))
	gameDirectionsRect3 = gameDirections3.get_rect(center = (WIDTH / 2, HEIGHT / 2 - 100))
	scoreSurface = game.font.render('Score ' + str(game.score), False, (255,255,255))
	scoreRect = scoreSurface.get_rect(center = (150, 50))
	livesSurface = game.font.render('Lives: ' + str(game.lives), False, (255,255,255))
	livesRect = livesSurface.get_rect(center = (WIDTH - 150,50))
	direction = pygame.math.Vector2()
	

	ENEMYLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(ENEMYLASER,800)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				game.gameActive = True
				game.respawnPlayer()
			if event.type == ENEMYLASER:
				game.enemyShoot()

		if game.gameActive: # If game is active
			screen.fill((30,30,30))
			game.run()
			scoreSurface = game.font.render('Score ' + str(game.score), False, (255,255,255))
			screen.blit(scoreSurface,scoreRect)
			livesSurface = game.font.render('Lives: ' + str(game.lives), False, (255,255,255))
			screen.blit(livesSurface, livesRect)
			pygame.display.flip()
			clock.tick(60)

			# Player control input
			keyPressed = pygame.key.get_pressed()

			if keyPressed[pygame.K_w]:
				direction.y = -1
			elif keyPressed[pygame.K_s]:
				direction.y = 1
			else:
				direction.y = 0

			if keyPressed[pygame.K_d]:
				direction.x = 1
			elif keyPressed[pygame.K_a]:
				direction.x = -1
			else:
				direction.x = 0

			if direction.magnitude() != 0:
				direction = direction.normalize()

			


		else:               # If game is inactive
			highScoreDisplay = game.font.render('High Score: ' + str(game.highScore), False, (255,255,255))
			highScoreDisplayRect = highScoreDisplay.get_rect(center = (WIDTH / 2, 50))
			screen.fill((30,30,30))
			screen.blit(highScoreDisplay,highScoreDisplayRect)
			screen.blit(gameName,gameNameRect)
			screen.blit(gameDirections,gameDirectionsRect)
			screen.blit(gameDirections2,gameDirectionsRect2)
			screen.blit(gameDirections3,gameDirectionsRect3)
			game.lives = 3
			game.playerSprite.reset()
			pygame.display.flip()
			
			
