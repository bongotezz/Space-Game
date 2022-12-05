import pygame, sys
from os import path
from player import *
from enemy import *
from random import choice, randint
from laser import *
from explosion import *
from pygame.locals import *
from button import Button

class Game:
    def __init__(self):
    	self.playerSprite = Player(bounds)
    	self.player = pygame.sprite.GroupSingle(self.playerSprite)

    	# Lives and score setup
    	self.lives = 3
    	self.extraLifePoints = 25000
    	self.extraLifeCounter = 1
    	self.score = 0
    	self.lastScore = 0
    	self.respawnTime = 200 # Used for delay between death and reapawn
    	self.font = pygame.font.Font('font/kenvector_future.ttf',50)
    	self.gameActive = False
    	self.gameOverTimer = 400
    	self.gameOverText = self.font.render('Game Over', False, (255,255,255))
    	self.gameOverTextRect = self.gameOverText.get_rect(center = (WIDTH / 2, HEIGHT / 2 + 100))
    	self.displayStageTimer = 150
    	self.stage = 1

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
    			elif enemyRows == 4:
    				ship = Enemy(bounds, 50 + (enemyOffset * (enemyColumns - 1)), 150 + (enemyOffset * (enemyRows - 1)), 'red2')
    			elif enemyRows == 3:
    				ship = Enemy(bounds, 50 + (enemyOffset * (enemyColumns - 1)), 150 + (enemyOffset * (enemyRows - 1)), 'green3')
    			elif enemyRows == 2:
    				ship = Enemy(bounds, 50 + (enemyOffset * (enemyColumns - 1)), 150 + (enemyOffset * (enemyRows - 1)), 'blue4')
    			elif enemyRows == 1:
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
    				self.playerHit()
    				
    	if self.bombExplosions and not self.holdFire:
    		for explosion in self.bombExplosions:
    			if pygame.sprite.spritecollide(explosion,self.player,False):
    				explosion.kill()
    				self.playerHit()
    				
    def endGame(self):
    	
    	self.gameOverTimer -= 1

    	screen.blit(self.gameOverText,self.gameOverTextRect)

    	if self.lives <= 0 and self.gameOverTimer <= 0:
    		self.gameActive = False
    		self.enemyLasers.empty()
    		self.enemies.empty()
    		self.bombers.empty()
    		self.bombs.empty()
    		self.bombExplosions.empty()
    		self.playerSprite.lasers.empty()
    		self.explosions.empty()

    		self.extraLifeCounter = 1
    		self.displayStageTimer = 150
    		self.stage = 1

    		highScores.append(self.score)
    		highScores.sort(reverse=True)
    		if len(highScores) > 10:
    			highScores.pop(-1)
    		file = open('Saves/HighScores.txt', 'w')
    		for score in highScores:
    			file.write(str(score) + '\n')
    		file.close() # closes file

    		self.lastScore = self.score
    		self.score = 0

    def enemyShoot(self):
    	if self.enemies.sprites():
    		if not self.holdFire and self.lives > 0:
    			randomEnemy = choice(self.enemies.sprites())
    			if randomEnemy.onScreen:
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
    			self.explosionSound.play()
    			self.explosionSound.play()
    			bomb.kill()

    def respawnTimer(self):
    	self.respawnTime -= 1
    	if self.respawnTime <= 0:
    		self.respawnTime = 200
    		self.holdFire = False
    		self.playerSprite.reset()

    def extraLifeCheck(self):
    	if self.extraLifePoints * self.extraLifeCounter <= self.score:
    		self.lives += 1
    		self.extraLifeCounter += 1

    def playerHit(self):
    	self.lives -= 1
    	self.holdFire = True

    	explosion = Explosion(self.playerSprite.rect.centerx,self.playerSprite.rect.centery,True)
    	self.explosions.add(explosion)
    	self.explosionSound.play()

    def displayStage(self):
    	stageText = self.font.render('Stage ' + str(self.stage), False, (255,255,255))
    	stageTextRect = stageText.get_rect(center = (WIDTH / 2, HEIGHT / 2 + 100))
    	if self.displayStageTimer >= 0:
    		screen.blit(stageText,stageTextRect)
    		self.displayStageTimer -= 1
    	else:
    		self.stage += 1
    		self.displayStageTimer = 150
    		self.spawnEnemies()

    def run(self):
    	if self.gameActive:
    		if not self.enemies:
    			self.displayStage()

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
    	
    		if not self.holdFire and self.lives > 0:
    			self.player.draw(screen)

    		self.enemyLasers.draw(screen)
    		self.enemies.draw(screen)
    		self.explosions.draw(screen)
    		self.bombers.draw(screen)
    		self.bombs.draw(screen)
    		self.bombExplosions.draw(screen)

    		self.checkCollisions()
    		self.extraLifeCheck()

    		if self.holdFire:
    			self.respawnTimer()

    		if self.lives <= 0:
    			self.endGame()

    def displayHighScores(self,highScores):
    	YPosition = 20
    	scoreText = self.font.render('High Scores', False,(255,255,255))
    	scoreTextRect = scoreText.get_rect(center = (bounds[0] / 2,YPosition))
    	screen.blit(scoreText,scoreTextRect)
    	YPosition += 90
    	i = 0
    	while i <= len(highScores) - 1:
    		scoreText = self.font.render(str(highScores[i]), False,(255,255,255))
    		scoreTextRect = scoreText.get_rect(center = (bounds[0] / 2,YPosition))
    		screen.blit(scoreText,scoreTextRect)
    		YPosition += 90
    		i += 1


if __name__ == '__main__':
	pygame.init()
	WIDTH = 900 # Screen width 900
	HEIGHT = 1000 # Screen height 1080
	bounds = [WIDTH, HEIGHT]
	screen = pygame.display.set_mode((bounds),RESIZABLE)
	clock = pygame.time.Clock()
	game = Game()
	scoreSurface = game.font.render('Score ' + str(game.score), False, (255,255,255))
	scoreRect = scoreSurface.get_rect(center = (150, 50))
	livesSurface = game.font.render('Lives: ' + str(game.lives), False, (255,255,255))
	livesRect = livesSurface.get_rect(center = (WIDTH - 150,50))
	ENEMYLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(ENEMYLASER,800)
	highScores = []
	direction = pygame.math.Vector2() # for player controls
	playerFire = False

	# screens
	backgroundSurface = pygame.image.load('Images/background2.png').convert_alpha()
	backgroundRect = backgroundSurface.get_rect(topleft = (0,0))
	splashSurface = pygame.image.load('Images/splashBackground.png').convert_alpha()
	splashSurfaceRect = splashSurface.get_rect(topleft = (0,0))
	controlsSurface = pygame.image.load('Images/controls.png').convert_alpha()
	controlsSurfaceRect = controlsSurface.get_rect(topleft = (0,0))
	creditsSurface = pygame.image.load('Images/credits.png').convert_alpha()
	creditsSurfaceRect = controlsSurface.get_rect(topleft = (0,0))
	screenDisplayed = 'none' # none is for splash screen. Controls, High Scores, and Credits are possibilities
	
	# button section
	buttons = pygame.sprite.Group()
	highScoreButton = Button(bounds, 'active', (50, HEIGHT - 250), 'High Scores')
	buttons.add(highScoreButton)
	controlsButton = Button(bounds, 'inactive', (50, HEIGHT - 200), 'Controls')
	buttons.add(controlsButton)
	creditsButton = Button(bounds, 'inactive', (50, HEIGHT - 150), 'Credits')
	buttons.add(creditsButton)

	backButtons = pygame.sprite.Group()
	backButton = Button(bounds, 'inactive', (WIDTH - 250, HEIGHT - 50), 'Back')
	backButtons.add(backButton)

	# controller setup
	joystickCount = pygame.joystick.get_count()
	if joystickCount != 0:
		controller = pygame.joystick.Joystick(0)
		controller.init()
		print(controller.get_name())

	def readHighScores():
		file = open('Saves/HighScores.txt', 'r')
		text = file.readlines()
		i = 0
		while i <= len(text) -1:
			score = int(text[i])
			highScores.append(score)
			if len(highScores) > 10:
				highScores.pop(-1)
			i += 1
		file.close()

	def eventHandling():
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # whole game code
				pygame.quit()
				sys.exit()

			if game.gameActive == False: # if the game is not active
				if (event.type == pygame.KEYDOWN and event.key == pygame.K_p) or (event.type == JOYBUTTONDOWN and (event.button == 9 or event.button == 7)):
					game.gameActive = True
					game.gameOverTimer = 400
					game.respawnPlayer()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

			if game.gameActive: # if game is active code
				playerFire = False
				direction.x = 0
				direction.y = 0

				if event.type == ENEMYLASER:
					game.enemyShoot()
				elif ((event.type == JOYBUTTONDOWN and (event.button == 1 or event.button == 0)) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)) and game.holdFire == False:
					playerFire = True
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # exits active game
					game.gameActive = False
					game.gameOverTimer = -1
					game.lives = 0
					game.score = 0
					game.endGame()

				game.player.update(direction,playerFire)

	def playerController(): # controls axis movement only
		if joystickCount != 0:
			if abs(controller.get_axis(0)) > 0.1:
				direction.x = controller.get_axis(0)
			if abs(controller.get_axis(1)) > 0.1:
				direction.y = controller.get_axis(1)

			if abs(controller.get_axis(0)) > 0.1 or abs(controller.get_axis(1)) > 0.1:
				game.player.update(direction,playerFire)

	readHighScores()

	while True:
		eventHandling()

		if game.gameActive: # If game is active
			screen.blit(backgroundSurface,backgroundRect)
			game.run()
			scoreSurface = game.font.render('Score ' + str(game.score), False, (255,255,255))
			screen.blit(scoreSurface,scoreRect)
			livesSurface = game.font.render('Lives: ' + str(game.lives), False, (255,255,255))
			screen.blit(livesSurface, livesRect)
			pygame.display.flip()
			clock.tick(60)

			keyPressed = pygame.key.get_pressed() # keyboard input for moving the ship

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

			if game.holdFire == False and keyPressed:
				game.player.update(direction,playerFire)

			playerController()

		elif game.gameActive == False and screenDisplayed == 'none':               # If game is inactive
			lastScoreDisplay = game.font.render('Last Score: ' + str(game.lastScore), False, (255,255,255))
			lastScoreDisplayRect = lastScoreDisplay.get_rect(center = (WIDTH / 2, HEIGHT - 50))
			screen.blit(splashSurface,splashSurfaceRect)
			screen.blit(lastScoreDisplay,lastScoreDisplayRect)
			game.lives = 3
			game.playerSprite.reset()
			buttons.update()
			buttons.draw(screen)
			for b in buttons:
				b.addLabel(screen)
				if b.clicked:
					b.clicked = False
					screenDisplayed = b.label
			pygame.display.flip()

		elif game.gameActive == False and screenDisplayed == 'High Scores':
			screen.blit(backgroundSurface,backgroundRect)
			game.displayHighScores(highScores)
			backButtons.update()
			backButtons.draw(screen)
			for b in backButtons:
				b.addLabel(screen)
				if b.clicked:
					b.clicked = False
					screenDisplayed = 'none'
			pygame.display.flip()

		elif game.gameActive == False and screenDisplayed == 'Controls':
			screen.blit(controlsSurface,controlsSurfaceRect)
			backButtons.update()
			backButtons.draw(screen)
			for b in backButtons:
				b.addLabel(screen)
				if b.clicked:
					b.clicked = False
					screenDisplayed = 'none'
			pygame.display.flip()

		elif game.gameActive == False and screenDisplayed == 'Credits':
			screen.blit(creditsSurface,creditsSurfaceRect)
			backButtons.update()
			backButtons.draw(screen)
			for b in backButtons:
				b.addLabel(screen)
				if b.clicked:
					b.clicked = False
					screenDisplayed = 'none'
			pygame.display.flip()


		
		
			
			
