import pygame
import sys
import random
import math
from pygame import mixer
import time

pygame.init()

#set game dispaly
s=pygame.display.set_mode((800,600))
pygame.display.set_caption('Shoot to aliens')

#set a logo
i=pygame.image.load('img/monster.png')
pygame.display.set_icon(i)


#set background music
mixer.music.load('img/bg.mid')
mixer.music.play(-1)

#player
playerImg = pygame.image.load('img/plspaceship.png') #player image
playerX=300 #x cordinate of the player(spaceship)
playerY = 480  #y cordinate of the player(spaceship)
playerX_change=0 

#enemies
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=7


for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('img/alien.png'))
    enemyImg.append(pygame.image.load('img/monster.png'))

    #generate random x and y position for enemies	
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))

	#generate  random speed for enemies
    enemyX_change.append(random.uniform(0.3,0.5))
    enemyY_change.append(40)


#bullet
bulletImg = pygame.image.load('img/mybullet.png')
bulletX = 0
bulletY = 480
bulletY_change=1
bulletX_change=1
bullet_state = 'ready'

score=0

font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

gofont= pygame.font.Font('freesansbold.ttf',70)

#alien craft
seImg = pygame.image.load('img/ufo.png')

#generate random x and y position for alien craft
strangeX = random.randint(0,700) 
strangeY = random.randint(15,120)

#alien craft movement
strangeY_change=45
strangeX_change=1

#all game elements add to the display

def alienCraft(x,y):
    s.blit(seImg,(x,y))



#game over function
def game_over(x,y):
    go_text= gofont.render('GAME OVER' ,True, (255,255,255))
    s.blit(go_text,(200,250))

#player function    
def player(x,y):
    s.blit(playerImg,(x,y))


#enemy function 
def enemy(x,y,i):
    s.blit(enemyImg[i],(x,y))

#bullet shooting function
def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    s.blit(bulletImg,(x+16,y))

#check collision 
def isCollision(playerX, playerY, enemyX, enemyY):

    #get the distance between a bullet and a enemy
    distance= math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY- bulletY, 2)) 
    
    if distance <27:
        return True
    else:
        return False

#check collision between craf and bullet
def iscollisionwithCraft(playerX, playerY, strangeX, strangeY):
    distancesb=math.sqrt(math.pow(craftX-bulletX, 2) + math.pow(craftY- bulletY, 2))
    if distancesb <27:
        return True
    else:
        return False

    
def show_score(x,y):
    scr= font.render('Scores : '+str(score) , True, (255,255,255))
    s.blit(scr, (x,y))
    
running=True

while True:
    s.fill((20,20,25))
  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.5

            if event.key == pygame.K_LEFT:
                playerX_change = -1.5

            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound('img/lnb.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                playerX_change =0

    playerX += playerX_change

   
    
    if playerX >= 736:
        playerX = 736
    if playerX <=0:
        playerX = 0

     
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change [i]

                        
        
                
                        
        if enemyX[i] > 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] <0 :
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
            
        enemy(enemyX[i], enemyY[i], i)

        if enemyY[i] > 430:
            for j in range(num_of_enemies):
                enemyY[j]=2000
                strangeY=2000
                game_over(200,250)
            
        collision = isCollision( bulletX, bulletY, enemyX[i], enemyY[i] )
        if collision:
            explosion= mixer.Sound('img/exp.wav')
            explosion.play()
            bulletY=480
            bullet_state='ready'
            enemyX[i]=random.randint(0,735)
            enemyY[i] = random.randint(50,150)
            
            
            score+=5

    collisionwithCraft = iscollisionwithCraft(playerX, playerY, craftX, craftY)
    if collisionwithCraft:
        explosions= mixer.Sound('img/exps.wav')
        explosions.play()
        bulletY=480
        bullet_state='ready'
        craftX=random.randint(0,735)
        craftY= random.randint(50,150)
        score+=10 
        
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bullet_state= 'ready'
        bulletY = 480

    
    craftX += craftX_change
    if craftX < 0:
        craftX_change = 0.8
        craftY += 45
    elif craftX > 760:
        craftX_change = -0.8
        craftY += 45

  
    if craftY >430:
        for j in range(num_of_enemies):               
            enemyY[j]=2000
        craftY=2000
        game_over(200,250)

    

    alienCraft(craftX,craftY)
        

    show_score(textX, textY)
    
    player(playerX, playerY)
    
    pygame.display.update()
     

    
        
