import pygame
import random
import math
from pygame import mixer

# initailize the pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))

# Background
bg = pygame.image.load('background_1.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


# Title and icon 
pygame.display.set_caption('Space Invaders!!')
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
eneImg = []
eneX = []
eneY = []
eneX_change = []
eneY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
	eneImg.append(pygame.image.load('enemy.png'))
	eneX.append(random.randint(0,736))
	eneY.append(random.randint(50,150))
	eneX_change.append(4)
	eneY_change.append(20)


# Bullet
## ready - cant see the bullet
## fire - the bullet is moving
buImg = pygame.image.load('bullet.png')
buX = 0
buY = 480
buX_change = 0
buY_change = 10
bu_state = 'ready'

#Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text

over_font = pygame.font.Font('MiddleAgesDeco_PERSONAL_USE.ttf', 64)

def show_score(x, y):
	score = font.render('Score :' + str(score_value), True, (150, 240, 20))
	screen.blit(score, (x, y))

def game_over_text():
	over_text = over_font.render('GAME OVER!!', True, (150, 20, 240))
	screen.blit(over_text, (110, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(eneImg[i], (x, y))

def fire_bullet(x, y):
    global bu_state
    bu_state = 'fire'
    screen.blit(buImg, (x + 16 , y + 10))
 
def isCollision(eneX, eneY, buX, buY):
	distance = math.sqrt((math.pow(eneX - buX, 2)) + (math.pow(eneY - buY, 2)))
	if distance < 27:
 		return True
	else:
 		return False


# Game Loop
running = True
while running:
    # RGB
    screen.fill((73, 46, 64))
    
    # Background Image
    screen.blit(bg, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
         
        # if keystroke is pressed check wheather its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bu_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    buX = playerX
                    fire_bullet( buX, buY)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    # checking for boundaries of spaceship so it doesnt go out of bounds
    playerX += playerX_change
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    # enemy movement
    for i in range(num_of_enemies):

    	# Game Over
    	if eneY[i] > 440:
    		for j in range(num_of_enemies):
    			eneY[j] = 2000
    		game_over_text()
    		break

    	eneX[i] += eneX_change[i]
    
    	if eneX[i] <= 0:
        	eneX_change[i] = 4
        	eneY[i] += eneY_change[i]
    	elif eneX[i] >= 736:
        	eneX_change[i] = -4
        	eneY[i] += eneY_change[i]
    	# Collision
    	collision = isCollision( eneX[i], eneY[i], buX, buY)
    	if collision:
    		exp_sound = mixer.Sound('explosion.wav')
    		exp_sound.play()
    		buY = 480
    		bu_state = 'ready'
    		score_value +=1
    		eneX[i] = random.randint(0,736)
    		eneY[i] = random.randint(50,150)
    	enemy(eneX[i], eneY[i], i)

    # bullet movement
    if buY <= 0:
        buY = 480
        bu_state = 'ready'
    
    if bu_state == 'fire':
        fire_bullet( buX, buY)
        buY -= buY_change
    

    
    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()

    
   

