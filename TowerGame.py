#
# Copyright Logan ALLEN 2015
# All rights reserved
#

import pygame
import random
import math
import sys
from pygame.locals import *
from Tower import Tower
from Bullet import Bullet
from Arrow import Arrow
from Bomb import Bomb
from Fireball import Fireball
from Iceball import Iceball
from Enemy import Enemy
from Levels import Levels
from Path1 import Path1
from Path2 import Path2
from Path3 import Path3
from Path4 import Path4

pygame.init()

screen = pygame.display.set_mode((840, 720))
pygame.display.set_caption("Tower Defenze")
transparent = pygame.Surface((840,720),pygame.SRCALPHA,32).convert_alpha()
background = pygame.image.load("images/background.png").convert_alpha()
grass = pygame.image.load("images/grass.png").convert_alpha()
space = pygame.image.load("images/space.png").convert_alpha()
minispace = pygame.image.load("images/miniSpace.png").convert_alpha()
topmenu = pygame.image.load("images/topMenu.png").convert_alpha()
botmenu = pygame.image.load("images/bottomMenu.png").convert_alpha()
screen.blit(background, (0, 0))
screenColor = (118,238,0)

# Sounds
chaching = pygame.mixer.Sound('sounds/chaching.wav')
spawn = pygame.mixer.Sound('sounds/enemyBlurp.wav')
enemyDie = pygame.mixer.Sound('sounds/die.wav')
hitBase = pygame.mixer.Sound('sounds/hitBase.wav')
gunshot = pygame.mixer.Sound('sounds/gunshot.wav')
arrows = pygame.mixer.Sound('sounds/arrows.wav')
cannon = pygame.mixer.Sound('sounds/cannon2.wav')
fireballSound = pygame.mixer.Sound('sounds/fireball.wav')
iceballSound = pygame.mixer.Sound('sounds/iceball.wav')

monster1image = pygame.image.load("images/monster1.png").convert_alpha()
monster2image = pygame.image.load("images/monster2.png").convert_alpha()
monster3image = pygame.image.load("images/monster3.png").convert_alpha()
monster4image = pygame.image.load("images/monster11.png").convert_alpha()
monster5image = pygame.image.load("images/monster12.png").convert_alpha()
monster6image = pygame.image.load("images/monster13.png").convert_alpha()

gold = 2100
prevGold = 2100
goldImage = pygame.image.load("images/gold.png").convert_alpha()
goldRect = goldImage.get_rect(center=(755, 50))
goldFont = pygame.font.SysFont(None, 26)
buttonFont = pygame.font.SysFont(None, 25)
shopFont = pygame.font.SysFont(None, 20)
levelFont = pygame.font.SysFont(None, 35)
earnedFont = pygame.font.SysFont(None, 25)

# Create Tower
xTower = 1300
yTower = 315
radiusTower = 200
tower = Tower(screen,xTower,yTower,radiusTower,1)
tower.rotateImages()
xTower2 = 1300
yTower2 = 315
tower2 = Tower(screen,xTower2,yTower2,radiusTower,2)
tower2.rotateImages()
placeTower = False
placeTower2 = False
towerIsSet = False
secondTower = False
placeSecondTower = False
placeSecondTower2 = False
tower2IsSet = False

# Create weapons
weapons = []
for w in range(0,6):
    weapons.append(False)

weaponDamage = []
weaponDamage.append(1.5)    # Bullet
weaponDamage.append(1)      # Arrow
weaponDamage.append(3)      # Bomb
weaponDamage.append(5)      # fireball
weaponDamage.append(8)      # Iceball

weaponPicked = []
for i in range(0,6):
    weaponPicked.append(False)

shopWeaponChoice = []
for x in range(0,9):
    shopWeaponChoice.append(False)

purchase = []
for x in range(0,9):
    purchase.append(False)

weaponCost = []
for x in range(100,600,100):
    weaponCost.append(x)
weaponCost.append(2000) #Health boost cost
weaponCost.append(250) #Tower Shooter cost
weaponCost.append(150) #Radius Increase cost
weaponCost.append(4000) #2nd Tower cost

imageBullet = pygame.image.load("images/bullet.png").convert_alpha()
imageArrow = pygame.image.load("images/arrows.png").convert_alpha()
imageBomb = pygame.image.load("images/bomb.png").convert_alpha()
imageFireball = pygame.image.load("images/fireball.png").convert_alpha()
imageIceball = pygame.image.load("images/iceball.png").convert_alpha()
imageBlackhole = pygame.image.load("images/blackhole.png").convert_alpha()
imageBase = pygame.image.load("images/base.png").convert_alpha()
imageMiniTower = pygame.image.load("images/miniTower.png").convert_alpha()
imageMiniTower2 = pygame.image.load("images/miniTower2.png").convert_alpha()
imageBoost = pygame.image.load("images/healthBoost.png").convert_alpha()
imageRadiusBoost = pygame.image.load("images/radiusBoost.png").convert_alpha()

# Enemy path
pathPics = []
pathPics.append(pygame.image.load("images/path1.png").convert_alpha())
pathPics.append(pygame.image.load("images/path3.png").convert_alpha())
pathPics.append(pygame.image.load("images/path2.png").convert_alpha())
pathPics.append(pygame.image.load("images/path4.png").convert_alpha())
paths = []
paths.append(Path1().getPath())
paths.append(Path3().getPath())
paths.append(Path2().getPath())
paths.append(Path4().getPath())
index = 0
pathChosen = paths[index]

numMonsters = [0,0,0,0,0,0]

# Instantiate gameStates
gameState = {}
gameState['info screen'] = True
gameState['start menu'] = False
gameState['wave'] = False
gameState['shop'] = False
gameState['won'] = False
gameState['lost'] = False


# Level instantiation
level = Levels().getLevels()
levelIndex = 0
bossLevel = False
bossDefeated = False

fireTimer = 0
fire = True
makingMonsters = False
monster1 = 0
monster2 = 0
monster3 = 0
monster4 = 0
monster5 = 0
monster6 = 0

gameButton = False
doneButton = False
buyButton = False
pathButton = False
gameButtonWord = ""
pauseGame = False

enemyTimer = 0
enemyTimers = {}
enemyTimers[0] = 50
enemyTimers[1] = 40
enemyTimers[2] = 30
enemyTimers[3] = 20
enemyTimers[4] = 10
enemyTimers[5] = 0
pauseTimer = 0

shopX = 850;
shopY = 150;
doneShopping = False

infoBox = pygame.Rect(175,-550,500,500)
boxDown = True
boxUp = False
playButton = False
finishInfo = False

# Create sprite groups
enemies = pygame.sprite.Group()
weaponGroup = pygame.sprite.Group()
weaponGroup2 = pygame.sprite.Group()
group = pygame.sprite.Group()


def draw_text(display_string, font, surface, x_pos, y_pos, color):
    text_display = font.render(display_string, 1, color)
    surface.blit(text_display, (x_pos, y_pos))

#   ****************** Weapon displays in top menu bar *******************
def drawTopMenu():

    screen.blit(topmenu,(0,0))

    # BULLET
    if purchase[0]:
        pygame.draw.rect(screen,(255,255,255),(20,25,37,37),0)
        draw_text("1",goldFont,screen,34,7,(255,255,255))
        if weaponPicked[0]:
            pygame.draw.rect(screen,(0,200,0),(20,25,37,37),3)
        else:
            pygame.draw.rect(screen,(0,0,0),(20,25,37,37),3)
    else:
        pygame.draw.rect(screen,(100,100,100),(20,25,37,37),0)
        pygame.draw.rect(screen,(0,0,0),(20,25,37,37),3)
        draw_text("1",goldFont,screen,34,7,(0,0,0))
    screen.blit(imageBullet,(26,32))

    # ARROWS
    if purchase[1]:
        pygame.draw.rect(screen,(255,255,255),(72,25,37,37),0)
        draw_text("2",goldFont,screen,86,7,(255,255,255))
        if weaponPicked[1]:
            pygame.draw.rect(screen,(0,200,0),(72,25,37,37),3)
        else:
            pygame.draw.rect(screen,(0,0,0),(72,25,37,37),3)
    else:
        pygame.draw.rect(screen,(100,100,100),(72,25,37,37),0)
        pygame.draw.rect(screen,(0,0,0),(72,25,37,37),3)
        draw_text("2",goldFont,screen,86,7,(0,0,0))
    screen.blit(imageArrow,(75,28))

    # BOMB
    if purchase[2]:
        pygame.draw.rect(screen,(255,255,255),(124,25,37,37),0)
        draw_text("3",goldFont,screen,138,7,(255,255,255))
        if weaponPicked[2]:
            pygame.draw.rect(screen,(0,200,0),(124,25,37,37),3)
        else:
            pygame.draw.rect(screen,(0,0,0),(124,25,37,37),3)
    else:
        pygame.draw.rect(screen,(100,100,100),(124,25,37,37),0)
        pygame.draw.rect(screen,(0,0,0),(124,25,37,37),3)
        draw_text("3",goldFont,screen,138,7,(0,0,0))
    screen.blit(imageBomb,(129,31))

    # FIREBALL
    if purchase[3]:
        pygame.draw.rect(screen,(255,255,255),(176,25,37,37),0)
        draw_text("4",goldFont,screen,190,7,(255,255,255))
        if weaponPicked[3]:
            pygame.draw.rect(screen,(0,200,0),(176,25,37,37),3)
        else:
            pygame.draw.rect(screen,(0,0,0),(176,25,37,37),3)
    else:
        pygame.draw.rect(screen,(100,100,100),(176,25,37,37),0)
        pygame.draw.rect(screen,(0,0,0),(176,25,37,37),3)
        draw_text("4",goldFont,screen,190,7,(0,0,0))
    screen.blit(imageFireball,(180,29))

    # ICEBALL
    if purchase[4]:
        pygame.draw.rect(screen,(255,255,255),(228,25,37,37),0)
        draw_text("5",goldFont,screen,242,7,(255,255,255))
        if weaponPicked[4]:
            pygame.draw.rect(screen,(0,200,0),(228,25,37,37),3)
        else:
            pygame.draw.rect(screen,(0,0,0),(228,25,37,37),3)
    else:
        pygame.draw.rect(screen,(100,100,100),(228,25,37,37),0)
        pygame.draw.rect(screen,(0,0,0),(228,25,37,37),3)
        draw_text("5",goldFont,screen,242,7,(0,0,0))
    screen.blit(imageIceball,(232,29))

    # Display Level
    if levelIndex>0:
        draw_text("Level "+str(levelIndex),levelFont,screen,370,25,(0,0,0))

    # Display gold
    screen.blit(goldImage,goldRect.topleft)
    draw_text(str(gold),goldFont,screen,778,40,(255,255,255))


def drawBotMenu():

    screen.blit(botmenu,(0,520))

    # Monster 1
    if numMonsters[0] > 0:
        colorz = (200,0,0)
    else:
        colorz = (100,100,100)
    pygame.draw.rect(screen,colorz,(14,672,37,37),0)
    pygame.draw.rect(screen,(0,0,0),(14,672,37,37),3)
    screen.blit(monster1image,(19,677))
    draw_text(str(numMonsters[0]),goldFont,screen,54,683,(0,0,0))

    # Monster 2
    if numMonsters[1] > 0:
        colorz = (200,0,0)
    else:
        colorz = (100,100,100)
    pygame.draw.rect(screen,colorz,(14+60+5,672,37,37),0)
    pygame.draw.rect(screen,(0,0,0),(14+60+5,672,37,37),3)
    screen.blit(monster2image,(19+60+5,677))
    draw_text(str(numMonsters[1]),goldFont,screen,54+60+5,683,(0,0,0))

    # EMonster 3
    if numMonsters[2] > 0:
        colorz = (200,0,0)
    else:
        colorz = (100,100,100)
    pygame.draw.rect(screen,colorz,(14+120+10,672,37,37),0)
    pygame.draw.rect(screen,(0,0,0),(14+120+10,672,37,37),3)
    screen.blit(monster3image,(19+120+10,677))
    draw_text(str(numMonsters[2]),goldFont,screen,54+120+10,683,(0,0,0))

    # EMonster 4
    if numMonsters[3] > 0:
        colorz = (200,0,0)
    else:
        colorz = (100,100,100)
    pygame.draw.rect(screen,colorz,(14+180+15,672,37,37),0)
    pygame.draw.rect(screen,(0,0,0),(14+180+15,672,37,37),3)
    screen.blit(monster4image,(19+180+15,677))
    draw_text(str(numMonsters[3]),goldFont,screen,54+180+15,683,(0,0,0))

    # EMonster 5
    if numMonsters[4] > 0:
        colorz = (200,0,0)
    else:
        colorz = (100,100,100)
    pygame.draw.rect(screen,colorz,(14+240+20,672,37,37),0)
    pygame.draw.rect(screen,(0,0,0),(14+240+20,672,37,37),3)
    screen.blit(monster5image,(19+240+20,677))
    draw_text(str(numMonsters[4]),goldFont,screen,54+240+20,683,(0,0,0))

    # EMonster 6
    if numMonsters[5] > 0:
        colorz = (200,0,0)
    else:
        colorz = (100,100,100)
    pygame.draw.rect(screen,colorz,(14+300+25,672,37,37),0)
    pygame.draw.rect(screen,(0,0,0),(14+300+25,672,37,37),3)
    screen.blit(monster6image,(19+300+25,677))
    draw_text(str(numMonsters[5]),goldFont,screen,54+300+25,683,(0,0,0))

    # Display gold earned
    if levelIndex>0:
        draw_text("Gold earned: "+str(gold-prevGold),earnedFont,screen,410,682,(255,227,164))




def drawScreen():
    global screen
    screen.fill(screenColor)
    screen.blit(space,(0,0))
    screen.blit(pathPics[index],(0,0))
    screen.blit(imageBlackhole,(-19,105))
    screen.blit(imageBase,(800,565))
    group.clear(screen, background)
    group.draw(screen)
    tower.drawImage(xTower,yTower)
    if secondTower:
        tower2.drawImage(xTower2,yTower2)
    drawTopMenu()
    tower.drawHealth()
    drawBotMenu()

drawScreen()

def createEnemy(monster):
    global enemies
    global group
    enemy = Enemy(screen,pathChosen[0][0],pathChosen[0][1],monster)
    enemy.setPath(pathChosen)
    enemies.add(enemy)
    group.add(enemy)
    group.add(enemy.health)

main_clock = pygame.time.Clock()

while True:

    # Frame Rate
    main_clock.tick(28)

    drawScreen()

    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

#   ******************* INPUT WHEN MOUSE IS CLICKED *****************

        if event.type == MOUSEBUTTONDOWN:
            locX = pygame.mouse.get_pos()[0]
            locY = pygame.mouse.get_pos()[1]

        elif event.type == MOUSEBUTTONUP:
            locX = pygame.mouse.get_pos()[0]
            locY = pygame.mouse.get_pos()[1]
            print(str(locX)+","+str(locY))
            gameButton = False
            pathButton = False
            playButton = False


#   *********************** INPUT DURING START MENU ************************
        if gameState['info screen']:

            if event.type == MOUSEBUTTONDOWN:
                # Switch game states to start menu
                if locX>595 and locX<595+63 and locY>infoBox.y+450 and locY<infoBox.y+483:
                    playButton = True


            if event.type == MOUSEBUTTONUP:
                # Switch game states to start menu
                if locX>595 and locX<595+63 and locY>infoBox.y+450 and locY<infoBox.y+483:
                    finishInfo = True


#   *********************** INPUT DURING START MENU ************************

        if gameState['start menu']:

            if event.type == MOUSEBUTTONDOWN:
                if locX > 625 and locX<625+94 and locY>673 and locY<673+34:
                    pathButton = True

                if locX > 733 and locX<733+94 and locY>673 and locY<673+34:
                    gameButton = True

            if event.type == MOUSEBUTTONUP:
                if locX > 625 and locX<625+94 and locY>673 and locY<673+34:
                    if index<len(paths)-1:
                        index += 1
                    else:
                        index = 0
                    pathChosen = paths[index]

                # Switch game states to shop
                if locX > 733 and locX<733+94 and locY>673 and locY<673+34:
                    gameState['start menu'] = False
                    gameState['shop'] = True
                    gameButtonWord = "  START"


#   ************************ INPUT DURING SHOPPING *************************

        elif gameState['shop']:

            if event.type == MOUSEBUTTONDOWN:
                # Set bullet choice to green
                if locX>shopX+12 and locX<shopX+49 and locY>205 and locY<242 and weaponCost[0]<=gold  and purchase[5]:
                    for x in range(0,len(shopWeaponChoice)):
                        shopWeaponChoice[x] = False
                    shopWeaponChoice[0] = True

                # Set arrow choice to green
                elif locX>shopX+12 and locX<shopX+49 and locY>205+65 and locY<242+65 and weaponCost[1]<=gold and purchase[5]:
                    for x in range(0,len(shopWeaponChoice)):
                        shopWeaponChoice[x] = False
                    shopWeaponChoice[1] = True

                # Set bomb choice to green
                elif locX>shopX+12 and locX<shopX+49 and locY>205+130 and locY<242+130 and weaponCost[2]<=gold and purchase[5]:
                    for x in range(0,len(shopWeaponChoice)):
                        shopWeaponChoice[x] = False
                    shopWeaponChoice[2] = True

                # Set fireball choice to green
                elif locX>shopX+12 and locX<shopX+49 and locY>205+195 and locY<242+195 and weaponCost[3]<=gold and purchase[5]:
                    for x in range(0,len(shopWeaponChoice)):
                        shopWeaponChoice[x] = False
                    shopWeaponChoice[3] = True

                # Set iceball choice to green
                elif locX>shopX+12 and locX<shopX+49 and locY>205+260 and locY<242+260 and weaponCost[4]<=gold and purchase[5]:
                    for x in range(0,len(shopWeaponChoice)):
                        shopWeaponChoice[x] = False
                    shopWeaponChoice[4] = True

				# Set Tower choice to green
                elif locX>shopX+200 and locX<shopX+236 and locY>205 and locY<242 and weaponCost[5]<=gold:
                    for x in range(0,len(shopWeaponChoice)):
                        shopWeaponChoice[x] = False
                    shopWeaponChoice[5] = True

                # Set HealthBoost choice to green
                elif locX>shopX+200 and locX<shopX+237 and locY>270 and locY<307 and weaponCost[6]<=gold and tower.health.health < 15:
                    for x in range(0,len(shopWeaponChoice)):
                        shopWeaponChoice[x] = False
                    shopWeaponChoice[6] = True

                # Set RadiusBoost choice to green
                elif locX>shopX+200 and locX<shopX+237 and locY>270+65 and locY<307+65 and weaponCost[7]<=gold and levelIndex >= 10 and purchase[5]:
                    for x in range(0,len(shopWeaponChoice)):
                        shopWeaponChoice[x] = False
                    shopWeaponChoice[7] = True

                # Set 2nd Tower choice to green
                elif locX>shopX+200 and locX<shopX+237 and locY>270+130 and locY<307+130 and weaponCost[8]<=gold and levelIndex >= 30:
                    for x in range(0,len(shopWeaponChoice)):
                        shopWeaponChoice[x] = False
                    shopWeaponChoice[8] = True

                elif(locX>shopX+15 and locX<shopX+63 and locY>560 and locY<585):
                    buyButton = True
                elif locX>shopX+325 and locX<shopX+390 and locY>560 and locY<585:
                    doneButton = True
                else:
                    for x in range(0,len(shopWeaponChoice)):
                        shopWeaponChoice[x] = False

                if locX > 733 and locX<733+94 and locY>673 and locY<673+34:
                    gameButton = True


            if event.type == MOUSEBUTTONUP:
                buyButton = False
                doneButton = False

                if placeTower2 and not towerIsSet:
                    xTower = locX
                    yTower = locY
                    placeTower2 = False
                    placeTower = False
                    towerIsSet = True
                if placeSecondTower2 and not tower2IsSet:
                    xTower2 = locX
                    yTower2 = locY
                    placeSecondTower2 = False
                    placeSecondTower = False
                    tower2IsSet = True

                # Buy button action
                if(locX>shopX+15 and locX<shopX+63 and locY>560 and locY<585):
                    for x in range(0,len(shopWeaponChoice)):
                        if shopWeaponChoice[x]:
                            if not purchase[x]:
                                if x==5:
                                    # Tower purchase
                                    placeTower = True
                                    gold -= weaponCost[x]
                                    purchase[x] = True
                                elif x==6:
                                    # Health boost
                                    gold -= weaponCost[x]
                                    tower.health.updateHealth(-5)
                                elif x==7:
                                    # Radius increase
                                    gold -= weaponCost[x]
                                    weaponCost[x] += 100
                                    tower.updateRadius(25)
                                    tower2.updateRadius(25)
                                elif x==8:
                                    # Second Tower
                                    placeSecondTower = True
                                    secondTower = True
                                    gold -= weaponCost[x]
                                    purchase[x] = True
                                    tower2 = Tower(screen,xTower2,yTower2,radiusTower,2)
                                    tower2.rotateImages()
                                else:
                                    purchase[x] = True
                                    gold -= weaponCost[x]
                                    for w in range(0,len(weapons)):
                                        weapons[w] = False
                                    weapons[x] = True
                                    for i in range(0,len(weaponPicked)):
                                        weaponPicked[i] = False
                                    weaponPicked[x] = True
                                chaching.play()
                    prevGold = gold


                # Done button pressed
                if(locX>shopX+325 and locX<shopX+390 and locY>560 and locY<585) and purchase[5] == True:
                    doneShopping = True

                if doneShopping:
                    # GameStart button pressed
                    if locX > 733 and locX<733+94 and locY>673 and locY<673+34:
                        gameButton = True
                        # Update level
                        if levelIndex < 51:
                            levelIndex += 1
                        elif levelIndex == 51:
                            levelIndex += 1
                            bossLevel = True

                        prevGold = gold

                        # Make monster type variables
                        monsterList = level[levelIndex]
                        monster1 = monsterList[0]
                        numMonsters[0] = monster1

                        monster2 = monsterList[1]
                        numMonsters[1] = monster2

                        monster3 = monsterList[2]
                        numMonsters[2] = monster3

                        monster4 = monsterList[3]
                        numMonsters[3] = monster4

                        monster5 = monsterList[4]
                        numMonsters[4] = monster5

                        monster6 = monsterList[5]
                        numMonsters[5] = monster6

                        totalMonsters = monster1+monster2+monster3+monster4+monster5+monster6

                        pygame.time.delay(1000)

                        gameState['shop'] = False
                        gameButton = False
                        gameState['wave'] = True
                        spawnMonsters = True
                        enemyTimer = 30
                        gameButtonWord = "  PAUSE"


#   ************************* INPUT DURING WAVES **************************

        elif gameState['wave']:
            if event.type == MOUSEBUTTONDOWN:

                if locX > 733 and locX<733+94 and locY>673 and locY<673+34:
                    gameButton = True

                # Option to select weapons vio CLICKING
                if purchase[0]:
                    if locX>20 and locX<57 and locY>25 and locY<62:
                        for w in range(0,len(weapons)):
                            weapons[w] = False
                        weapons[0] = True
                        for i in range(0,len(weaponPicked)):
                            weaponPicked[i] = False
                        weaponPicked[0] = True

                if purchase[1]:
                    if locX>20+52 and locX<57+52 and locY>25 and locY<62:
                        for w in range(0,len(weapons)):
                            weapons[w] = False
                        weapons[1] = True
                        for i in range(0,len(weaponPicked)):
                            weaponPicked[i] = False
                        weaponPicked[1] = True

                if purchase[2]:
                    if locX>20+104 and locX<57+104 and locY>25 and locY<62:
                        for w in range(0,len(weapons)):
                            weapons[w] = False
                        weapons[2] = True
                        for i in range(0,len(weaponPicked)):
                            weaponPicked[i] = False
                        weaponPicked[2] = True

                if purchase[3]:
                    if locX>20+156 and locX<57+156 and locY>25 and locY<62:
                        for w in range(0,len(weapons)):
                            weapons[w] = False
                        weapons[3] = True
                        for i in range(0,len(weaponPicked)):
                            weaponPicked[i] = False
                        weaponPicked[3] = True

                if purchase[4]:
                    if locX>20+208 and locX<57+208 and locY>25 and locY<62:
                        for w in range(0,len(weapons)):
                            weapons[w] = False
                        weapons[4] = True
                        for i in range(0,len(weaponPicked)):
                            weaponPicked[i] = False
                        weaponPicked[4] = True

                # Upon mouse click, fire bullets in correct direction
                if fire and not pauseGame:
                    if locX>0 and locX<840 and locY>74 and locY<660:
                        if weapons[0]:
                            # Bullet = 0
                            gunshot.play()
                            bullet = Bullet(screen,xTower,yTower,tower.angle)
                            bullet.rotateImages()
                            bullet.setDirection()
                            weaponGroup.add(bullet)
                            group.add(bullet)
                            if tower2IsSet:
                                bullet = Bullet(screen,xTower2,yTower2,tower2.angle)
                                bullet.rotateImages()
                                bullet.setDirection()
                                weaponGroup2.add(bullet)
                                group.add(bullet)
                        elif weapons[1]:
                            # Arrows = 1
                            arrows.play()
                            arrow1 = Arrow(screen,xTower,yTower,tower.angle)
                            arrow1.rotateImages()
                            arrow1.setDirection()
                            weaponGroup.add(arrow1)
                            group.add(arrow1)
                            arrow2 = Arrow(screen,xTower,yTower,tower.angle+7)
                            arrow2.rotateImages()
                            arrow2.setDirection()
                            weaponGroup.add(arrow2)
                            group.add(arrow2)
                            arrow3 = Arrow(screen,xTower,yTower,tower.angle-7)
                            arrow3.rotateImages()
                            arrow3.setDirection()
                            weaponGroup.add(arrow3)
                            group.add(arrow3)
                            if tower2IsSet:
                                arrow1 = Arrow(screen,xTower2,yTower2,tower2.angle)
                                arrow1.rotateImages()
                                arrow1.setDirection()
                                weaponGroup2.add(arrow1)
                                group.add(arrow1)
                                arrow2 = Arrow(screen,xTower2,yTower2,tower2.angle+7)
                                arrow2.rotateImages()
                                arrow2.setDirection()
                                weaponGroup2.add(arrow2)
                                group.add(arrow2)
                                arrow3 = Arrow(screen,xTower2,yTower2,tower2.angle-7)
                                arrow3.rotateImages()
                                arrow3.setDirection()
                                weaponGroup2.add(arrow3)
                                group.add(arrow3)
                        elif weapons[2]:
                            # Bomb = 2
                            cannon.play()
                            bomb = Bomb(screen,xTower,yTower,tower.angle)
                            weaponGroup.add(bomb)
                            group.add(bomb)
                            if tower2IsSet:
                                bomb = Bomb(screen,xTower2,yTower2,tower2.angle)
                                weaponGroup2.add(bomb)
                                group.add(bomb)

                        elif weapons[3]:
                            # Fireball
                            fireballSound.play()
                            fireball = Fireball(screen,xTower,yTower,tower.angle)
                            weaponGroup.add(fireball)
                            group.add(fireball)
                            if tower2IsSet:
                                fireball = Fireball(screen,xTower2,yTower2,tower2.angle)
                                weaponGroup2.add(fireball)
                                group.add(fireball)
                        elif weapons[4]:
                            # Iceball
                            iceballSound.play()
                            iceball = Iceball(screen,xTower,yTower,tower.angle)
                            weaponGroup.add(iceball)
                            group.add(iceball)
                            if tower2IsSet:
                                iceball = Iceball(screen,xTower2,yTower2,tower2.angle)
                                weaponGroup2.add(iceball)
                                group.add(iceball)
                        fire = False
                        fireTimer = 0

            # Pause Button
            if event.type == MOUSEBUTTONUP:
                if locX > 733 and locX<733+94 and locY>673 and locY<673+34:
                    if pauseGame:
                        pygame.time.delay(1000)
                        pauseGame = False
                    else:
                        pauseGame = True

            # Option to select weapons via KEYS
            if event.type == KEYDOWN:
                # Bullets
                if purchase[0]:
                    if event.key == K_1:
                        for w in range(0,len(weapons)):
                            weapons[w] = False
                        weapons[0] = True
                        for i in range(0,len(weaponPicked)):
                            weaponPicked[i] = False
                        weaponPicked[0] = True
                # Arrows
                if purchase[1]:
                    if event.key == K_2:
                        for w in range(0,len(weapons)):
                            weapons[w] = False
                        weapons[1] = True
                        for i in range(0,len(weaponPicked)):
                            weaponPicked[i] = False
                        weaponPicked[1] = True
                # Bomb
                if purchase[2]:
                    if event.key == K_3:
                        for w in range(0,len(weapons)):
                            weapons[w] = False
                        weapons[2] = True
                        for i in range(0,len(weaponPicked)):
                            weaponPicked[i] = False
                        weaponPicked[2] = True
                # Fireball
                if purchase[3]:
                    if event.key == K_4:
                        for w in range(0,len(weapons)):
                            weapons[w] = False
                        weapons[3] = True
                        for i in range(0,len(weaponPicked)):
                            weaponPicked[i] = False
                        weaponPicked[3] = True
                # Iceball
                if purchase[4]:
                    if event.key == K_5:
                        for w in range(0,len(weapons)):
                            weapons[w] = False
                        weapons[4] = True
                        for i in range(0,len(weaponPicked)):
                            weaponPicked[i] = False
                        weaponPicked[4] = True


#   ******************** GAME STATE FOR INFO SCREEN ********************

    if gameState['info screen']:

        transparent.fill((0,100,100,150))
        screen.blit(transparent,(0,0))

        # Show info about the game
        pygame.draw.rect(screen,(200,200,200),infoBox)
        pygame.draw.rect(screen,(0,0,0),(infoBox.x,infoBox.y,infoBox.width,infoBox.height),4)

        if boxDown:
            infoBox.y += main_clock.get_time()/5    # dividing = SLOWER
            if infoBox.y > 150:
                boxDown = False
                boxUp = True
        if boxUp:
            infoBox.y -= main_clock.get_time()/8
            if infoBox.y < 110:
                boxUp = False

        if finishInfo:
            infoBox.y -= 10
            if infoBox.y <= -600:
                finishInfo = False
                gameState['info screen'] = False
                gameState['start menu'] = True
                gameButtonWord = "SET Path"

        pygame.draw.rect(screen,(105,0,205),(infoBox.x+130,infoBox.y+20,infoBox.width-260,50),0)
        screen.blit(minispace,(infoBox.x+130,infoBox.y+20))
        pygame.draw.rect(screen,(0,0,0),(infoBox.x+130,infoBox.y+20,infoBox.width-260,50),3)
        draw_text("Tower Defenze!",levelFont,screen,infoBox.x+155,infoBox.y+30,(255,255,255))
        instructions = ">> Defend your space station from enemies"
        instructions2 = "   sent from the black hole."
        instructions3 = ">> Buy towers, weapons, and shoot your way"
        instructions4 = "   to victory!"
        draw_text("INSTRUCTIONS:",earnedFont,screen,infoBox.x+50,infoBox.y+100,(0,0,50))
        draw_text(instructions,earnedFont,screen,infoBox.x+70,infoBox.y+130,(0,0,50))
        draw_text(instructions2,earnedFont,screen,infoBox.x+70,infoBox.y+160,(0,0,50))
        draw_text(instructions3,earnedFont,screen,infoBox.x+70,infoBox.y+190,(0,0,50))
        draw_text(instructions4,earnedFont,screen,infoBox.x+70,infoBox.y+220,(0,0,50))

        #button is pressed
        if playButton:
            gameColor = (255,255,255)
        #button not pressed
        else:
            gameColor = (0,0,0)
        pygame.draw.rect(screen,(160,0,0),(595,infoBox.y+450,63,34),0)
        pygame.draw.rect(screen,gameColor,(595,infoBox.y+450,63,34),3)
        draw_text("PLAY",buttonFont,screen,605,infoBox.y+459,gameColor)



#   *********************** GAME STATE FOR MENU ************************

    elif gameState['start menu']:

        #button is pressed
        if pathButton:
            pathColor = (255,255,255)
        #button not pressed
        else:
            pathColor = (0,0,0)
        pygame.draw.rect(screen,(160,0,0),(625,673,94,34),0)
        pygame.draw.rect(screen,pathColor,(625,673,94,34),3)
        draw_text("CHANGE",buttonFont,screen,635,682,pathColor)


#   ********************* GAME STATE FOR SHOPPING **********************

    elif gameState['shop']:

        if placeTower2 and not towerIsSet:
            xTower = pygame.mouse.get_pos()[0]
            yTower = pygame.mouse.get_pos()[1]
        if placeSecondTower2 and not tower2IsSet:
            xTower2 = pygame.mouse.get_pos()[0]
            yTower2 = pygame.mouse.get_pos()[1]


        # Draw shopping menu
        if doneShopping:
            if shopX <= 848:
                shopX += 4
            if shopX >= 848:
                placeTower2 = True
                placeSecondTower2 = True
        elif placeTower and not towerIsSet:
            if shopX <= 848:
                shopX += 4
            if shopX >= 848:
                placeTower2 = True
        elif placeSecondTower and not tower2IsSet:
            if shopX <= 848:
                shopX += 4
            if shopX >= 848:
                placeSecondTower2 = True
        else:
            if shopX >= 402:
                shopX -= 4


        pygame.draw.rect(screen,(176,226,255),(shopX,shopY,400,445),0)
        pygame.draw.rect(screen,(0,0,0),(shopX,shopY,400,445),4)

        # Shop Title
        #r = random.randrange(0,255)
        #g = random.randrange(0,255)
        pygame.draw.line(screen,(0,0,0),(shopX+160,178),(shopX+232,178),3)
        draw_text("SHOP",buttonFont,screen,shopX+172,158,(0,0,0))

        # Draw done button
        if doneButton:
            colorDone = (0,200,0)
            colorDone2 = (255,255,255)
        else:
            colorDone = (255,255,255)
            colorDone2 = (0,0,0)
        pygame.draw.rect(screen,colorDone,(shopX+325,560,65,25),0)
        pygame.draw.rect(screen,colorDone2,(shopX+325,560,65,25),2)
        draw_text("DONE",buttonFont,screen,shopX+332,565,colorDone2)

        # Draw Buy button
        if buyButton:
            colorBuy = (0,200,0)
            colorBuy2 = (255,255,255)
        else:
            colorBuy = (255,255,255)
            colorBuy2 = (0,0,0)
        pygame.draw.rect(screen,colorBuy,(shopX+15,560,48,25),0)
        pygame.draw.rect(screen,colorBuy2,(shopX+15,560,48,25),2)
        draw_text("BUY",buttonFont,screen,shopX+22,565,colorBuy2)

        # Weapons List ******

        # BULLET
        if purchase[0]:
            pygame.draw.rect(screen,(255,255,255),(shopX+12,205,37,37),0)
            color = (238,201,0)
        elif weaponCost[0] <= gold and purchase[5]:
            pygame.draw.rect(screen,(255,255,255),(shopX+12,205,37,37),0)
            if shopWeaponChoice[0]:
                color = (0,200,0)
            else:
                color = (0,0,0)
        else:
            pygame.draw.rect(screen,(100,100,100),(shopX+12,205,37,37),0)
            color = (0,0,0)
        draw_text("Bullet",shopFont,screen,shopX+10,190,(0,0,0))
        pygame.draw.rect(screen,color,(shopX+12,205,37,37),3)
        screen.blit(imageBullet,(shopX+18,211))
        draw_text("Damage: "+str(weaponDamage[0]),shopFont,screen,shopX+55,208,(255,255,255))
        draw_text("Cost: "+str(weaponCost[0]),shopFont,screen,shopX+55,225,(255,255,255))

        # Arrows
        if purchase[1]:
            pygame.draw.rect(screen,(255,255,255),(shopX+12,205+65,37,37),0)
            color = (238,201,0)
        elif weaponCost[1] <= gold and purchase[5]:
            pygame.draw.rect(screen,(255,255,255),(shopX+12,205+65,37,37),0)
            if shopWeaponChoice[1]:
                color = (0,200,0)
            else:
                color = (0,0,0)
        else:
            pygame.draw.rect(screen,(100,100,100),(shopX+12,205+65,37,37),0)
            color = (0,0,0)
        draw_text("Arrows",shopFont,screen,shopX+10,190+65,(0,0,0))
        pygame.draw.rect(screen,color,(shopX+12,205+65,37,37),3)
        screen.blit(imageArrow,(shopX+16,211+63))
        draw_text("Damage: "+str(weaponDamage[1])+"(x3)",shopFont,screen,shopX+55,208+65,(255,255,255))
        draw_text("Cost: "+str(weaponCost[1]),shopFont,screen,shopX+55,225+65,(255,255,255))

        # Bomb
        if purchase[2]:
            pygame.draw.rect(screen,(255,255,255),(shopX+12,205+130,37,37),0)
            color = (238,201,0)
        elif weaponCost[2] <= gold and purchase[5]:
            pygame.draw.rect(screen,(255,255,255),(shopX+12,205+130,37,37),0)
            if shopWeaponChoice[2]:
                color = (0,200,0)
            else:
                color = (0,0,0)
        else:
            pygame.draw.rect(screen,(100,100,100),(shopX+12,205+130,37,37),0)
            color = (0,0,0)
        draw_text("Bomb",shopFont,screen,shopX+10,190+130,(0,0,0))
        pygame.draw.rect(screen,color,(shopX+12,205+130,37,37),3)
        screen.blit(imageBomb,(shopX+17,211+131))
        draw_text("Damage: "+str(weaponDamage[2]),shopFont,screen,shopX+55,208+130,(255,255,255))
        draw_text("Cost: "+str(weaponCost[2]),shopFont,screen,shopX+55,225+130,(255,255,255))

        # Fireball
        if purchase[3]:
            pygame.draw.rect(screen,(255,255,255),(shopX+12,205+195,37,37),0)
            color = (238,201,0)
        elif weaponCost[3] <= gold and purchase[5]:
            pygame.draw.rect(screen,(255,255,255),(shopX+12,205+195,37,37),0)
            if shopWeaponChoice[3]:
                color = (0,200,0)
            else:
                color = (0,0,0)
        else:
            pygame.draw.rect(screen,(100,100,100),(shopX+12,205+195,37,37),0)
            color = (0,0,0)
        draw_text("Fireball",shopFont,screen,shopX+10,190+195,(0,0,0))
        pygame.draw.rect(screen,color,(shopX+12,205+195,37,37),3)
        screen.blit(imageFireball,(shopX+16,211+194))
        draw_text("Damage: "+str(weaponDamage[3]),shopFont,screen,shopX+55,208+195,(255,255,255))
        draw_text("Cost: "+str(weaponCost[3]),shopFont,screen,shopX+55,225+195,(255,255,255))

        # Iceball
        if purchase[4]:
            pygame.draw.rect(screen,(255,255,255),(shopX+12,205+260,37,37),0)
            color = (238,201,0)
        elif weaponCost[4] <= gold and purchase[5]:
            pygame.draw.rect(screen,(255,255,255),(shopX+12,205+260,37,37),0)
            if shopWeaponChoice[4]:
                color = (0,200,0)
            else:
                color = (0,0,0)
        else:
            pygame.draw.rect(screen,(100,100,100),(shopX+12,205+260,37,37),0)
            color = (0,0,0)
        draw_text("Iceball",shopFont,screen,shopX+10,190+260,(0,0,0))
        pygame.draw.rect(screen,color,(shopX+12,205+260,37,37),3)
        screen.blit(imageIceball,(shopX+16,211+259))
        draw_text("Damage: "+str(weaponDamage[4]),shopFont,screen,shopX+55,208+260,(255,255,255))
        draw_text("Cost: "+str(weaponCost[4]),shopFont,screen,shopX+55,225+260,(255,255,255))

        # TOWER
        if purchase[5]:
            pygame.draw.rect(screen,(255,255,255),(shopX+200,205,37,37),0)
            color = (238,201,0)
        elif weaponCost[5] <= gold:
            pygame.draw.rect(screen,(255,255,255),(shopX+200,205,37,37),0)
            if shopWeaponChoice[5]:
                color = (0,200,0)
            else:
                color = (0,0,0)
        elif weaponCost[5] > gold:
            pygame.draw.rect(screen,(100,100,100),(shopX+200,205,37,37),0)
            color = (0,0,0)
        draw_text("Tower",shopFont,screen,shopX+195,190,(0,0,0))
        pygame.draw.rect(screen,color,(shopX+200,205,37,37),3)
        screen.blit(imageMiniTower,(shopX+191,200))
        draw_text("Info: Shoot enemies!",shopFont,screen,shopX+245,208,(255,255,255))
        draw_text("Cost: "+str(weaponCost[5]),shopFont,screen,shopX+245,225,(255,255,255))

        # HEALTH BOOST
        if weaponCost[6] <= gold and tower.health.health < 15:
            pygame.draw.rect(screen,(255,255,255),(shopX+200,270,37,37),0)
            if shopWeaponChoice[6]:
                color = (0,200,0)
            else:
                color = (0,0,0)
        else:
            pygame.draw.rect(screen,(100,100,100),(shopX+200,270,37,37),0)
            color = (0,0,0)
        draw_text("+Health",shopFont,screen,shopX+191,255,(0,0,0))
        pygame.draw.rect(screen,color,(shopX+200,270,37,37),3)
        screen.blit(imageBoost,(shopX+203,273))
        draw_text("Health Boost: 25",shopFont,screen,shopX+245,273,(255,255,255))
        draw_text("Cost: "+str(weaponCost[6]),shopFont,screen,shopX+245,290,(255,255,255))

        # Radius
        if weaponCost[7] <= gold and levelIndex >= 10 and purchase[5]:
            pygame.draw.rect(screen,(255,255,255),(shopX+200,270+65,37,37),0)
            if shopWeaponChoice[7]:
                color = (0,200,0)
            else:
                color = (0,0,0)
        else:
            pygame.draw.rect(screen,(100,100,100),(shopX+200,270+65,37,37),0)
            color = (0,0,0)
        draw_text("+Radius (After level 10)",shopFont,screen,shopX+191,255+65,(0,0,0))
        pygame.draw.rect(screen,color,(shopX+200,270+65,37,37),3)
        screen.blit(imageRadiusBoost,(shopX+204,273+65))
        draw_text("Radius Increase: 25",shopFont,screen,shopX+245,273+65,(255,255,255))
        draw_text("Cost: "+str(weaponCost[7]),shopFont,screen,shopX+245,290+65,(255,255,255))

        # Tower 2
        if purchase[8]:
            pygame.draw.rect(screen,(255,255,255),(shopX+200,270+130,37,37),0)
            color = (238,201,0)
        elif weaponCost[8] <= gold and levelIndex >= 30:
            pygame.draw.rect(screen,(255,255,255),(shopX+200,270+130,37,37),0)
            if shopWeaponChoice[8]:
                color = (0,200,0)
            else:
                color = (0,0,0)
        else:
            pygame.draw.rect(screen,(100,100,100),(shopX+200,270+130,37,37),0)
            color = (0,0,0)
        draw_text("Tower 2 (After level 30)",shopFont,screen,shopX+191,255+130,(0,0,0))
        pygame.draw.rect(screen,color,(shopX+200,270+130,37,37),3)
        screen.blit(imageMiniTower2,(shopX+191,273+123))
        draw_text("Radius Increase: 25",shopFont,screen,shopX+245,273+130,(255,255,255))
        draw_text("Cost: "+str(weaponCost[8]),shopFont,screen,shopX+245,290+130,(255,255,255))


#   ************************* GAME STATE FOR WAVE **************************

    elif gameState['wave']:

        keys = pygame.key.get_pressed()

        if not pauseGame:
            if spawnMonsters:
                for i in range(0,6):
                    enemyTimers[i] += 1

                if enemyTimers[0]>55 and monster1 > 0:
                    createEnemy(1)
                    monster1 -= 1
                    enemyTimers[0] = 0
                    spawn.play()
                    totalMonsters -= 1
                    spawnMonsters = totalMonsters > 0
                if enemyTimers[1]>55 and monster2 > 0 and monster1<monsterList[0]/3:
                    createEnemy(2)
                    monster2 -= 1
                    enemyTimers[1] = 0
                    spawn.play()
                    totalMonsters -= 1
                    spawnMonsters = totalMonsters > 0
                if enemyTimers[2]>55 and monster3 > 0 and monster2<monsterList[1]/3:
                    createEnemy(3)
                    monster3 -= 1
                    enemyTimers[2] = 0
                    spawn.play()
                    totalMonsters -= 1
                    spawnMonsters = totalMonsters > 0
                if enemyTimers[3]>60 and monster4 > 0 and monster3<monsterList[2]/3:
                    createEnemy(4)
                    monster4 -= 1
                    enemyTimers[3] = 0
                    spawn.play()
                    totalMonsters -= 1
                    spawnMonsters = totalMonsters > 0
                if enemyTimers[4]>60 and monster5 > 0 and monster4<monsterList[3]/2:
                    createEnemy(5)
                    monster5 -= 1
                    enemyTimers[4] = 0
                    spawn.play()
                    totalMonsters -= 1
                    spawnMonsters = totalMonsters > 0
                if enemyTimers[5]>60 and monster6 > 0 and monster5<monsterList[4]/2:
                    createEnemy(6)
                    monster6 -= 1
                    enemyTimers[5] = 0
                    spawn.play()
                    totalMonsters -= 1
                    spawnMonsters = totalMonsters > 0

            fireTimer += main_clock.get_time()
            if weaponPicked[0]:
                if fireTimer >= 200:
                    fire = True
            elif weaponPicked[1]:
                if fireTimer >= 300:
                    fire = True
            elif weaponPicked[2]:
                if fireTimer >= 450:
                    fire = True
            elif weaponPicked[3]:
                if fireTimer >= 400:
                    fire = True
            elif weaponPicked[4]:
                if fireTimer >= 400:
                    fire = True

            # Move weapon
            for b in weaponGroup:
                b.move()
                vector = pygame.math.Vector2((b.x-tower.x),(b.y-tower.y))
                if math.sqrt(vector[0]*vector[0] + vector[1]*vector[1]) > tower.radius:
                    weaponGroup.remove(b)
                    group.remove(b)

            # Move weapon 2
            for b in weaponGroup2:
                b.move()
                vector = pygame.math.Vector2((b.x-tower2.x),(b.y-tower2.y))
                if math.sqrt(vector[0]*vector[0] + vector[1]*vector[1]) > tower2.radius:
                    weaponGroup2.remove(b)
                    group.remove(b)

            # Move enemies
            for e in enemies:
                e.checkReachPoint()
                e.move()
                if e.inflictDamage:
                    hitBase.play()
                    tower.hurt(e.damage)
                if not e.alive:
                    if e.health.health == 0:
                        gold += e.value
                    numMonsters[e.monsterType] -= 1
                    enemies.remove(e)
                    enemyDie.play()
                    group.remove(e.health)
                    group.remove(e)

            # Weapon collision detection
            collideDict = pygame.sprite.groupcollide(weaponGroup,enemies,True,False)
            for weapon in collideDict.keys():
                for enem in collideDict[weapon]:
                    if weapons[0]:
                        enem.hit(weaponDamage[0])
                    elif weapons[1]:
                        enem.hit(weaponDamage[1])
                    elif weapons[2]:
                        enem.hit(weaponDamage[2])
                    elif weapons[3]:
                        enem.hit(weaponDamage[3])
                    elif weapons[4]:
                        enem.hit(weaponDamage[4])
                    break
            # Weapon 2 collision detection for second tower
            if tower2IsSet:
                collideDict = pygame.sprite.groupcollide(weaponGroup2,enemies,True,False)
                for weapon in collideDict.keys():
                    for enem in collideDict[weapon]:
                        if weapons[0]:
                            enem.hit(weaponDamage[0])
                        elif weapons[1]:
                            enem.hit(weaponDamage[1])
                        elif weapons[2]:
                            enem.hit(weaponDamage[2])
                        elif weapons[3]:
                            enem.hit(weaponDamage[3])
                        elif weapons[4]:
                            enem.hit(weaponDamage[4])
                        break

        # Update tower angle
        tower.updateAngle(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        tower2.updateAngle(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

        if len(enemies) == 0 and totalMonsters == 0:
            #print("Finished wave")
            gameState['wave'] = False
            if bossLevel:
                gameState['won'] = True
            else:
                gameState['shop'] = True
                doneShopping = False
                gameButtonWord = "  START"

            weaponGroup.clear(screen, background)
            weaponGroup2.clear(screen, background)
            group.empty()
            weaponGroup.empty()
            weaponGroup2.empty()

        elif tower.health.health == 0:
            gameState['wave'] = False
            gameState['lost'] = True


    #   ********************** GAME STATE FOR WON **********************




#   *********************************************************************
#   ********************* CODE THATS RUN ALL THE TIME *******************
#   *********************************************************************

    #button is pressed
    if gameButton:
        gameColor = (255,255,255)
    #button not pressed
    else:
        gameColor = (0,0,0)
    pygame.draw.rect(screen,(160,0,0),(733,673,94,34),0)
    pygame.draw.rect(screen,gameColor,(733,673,94,34),3)
    draw_text(gameButtonWord,buttonFont,screen,743,682,gameColor)

    # Update the screen
    pygame.display.update()

# END 