import pygame
import random
import math
from pygame import mixer

# initialize application
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('./images/background.png')

# background sound
mixer.music.load('./sounds/turing.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption('AnimaLogic')
icon = pygame.image.load('./images/giraffe (1).png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('./images/elephant (1).png')
# playerImg = pygame.transform.rotate(playerImg, 180)
playerX = 368
playerY = 40
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./images/hunter (1).png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(380, 480))
    enemyX_change.append(4)
    enemyY_change.append(-40)

# bullet
bulletImg = pygame.image.load('./images/drop.png')
bulletX = 0
bulletY = 40
bulletX_change = 0
bulletY_change = 10
# ready state = cant see on screen; fire = bullet is moving
bullet_state = 'ready'

# score board
score_value = 0
font = pygame.font.Font('./fonts/Roboto-Bold.ttf', 40)
textX = 10
textY = 10

over_font = pygame.font.Font('./fonts/Roboto-Bold.ttf', 80)

def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 20))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game over
def game_over_text():
    over_text = over_font.render('GAME OVER', True, (250, 20, 20))
    screen.blit(over_text, (200, 250))

# game loop
running = True
while running:

    # RGB values for background
    screen.fill((210, 180, 140))

    # background image
    screen.blit(background, (0, 0))

    # event loop
    for event in pygame.event.get():
        # allows app to quit when x is clicked
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('./sounds/elephant.wav')
                    bullet_sound.set_volume(0.11)
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # player boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy move
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] < 80:
            for j in range(num_of_enemies):
                enemyY[j] = -200
            playerY = 700
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 52
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(380, 480)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change
    if bulletY >= 600:
        bullet_state = 'ready'
        bulletY = 52



    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
