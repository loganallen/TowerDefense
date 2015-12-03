# Program Base!!!

import pygame
import random
import math
import sys
from pygame.locals import *
from Tower import Tower

pygame.init()

screen = pygame.display.set_mode((840, 720))
#background = pygame.Surface((740,540),0,screen)
background = pygame.image.load("images/background.png").convert_alpha()
grass = pygame.image.load("images/grass.png").convert_alpha()
space = pygame.image.load("images/space.png").convert_alpha()
topmenu = pygame.image.load("images/topMenu.png").convert_alpha()
botmenu = pygame.image.load("images/bottomMenu.png").convert_alpha()
path1 = pygame.image.load("images/path1.png").convert_alpha()
screen.blit(background, (0, 0))
screenColor = (118,238,0)

# Create Tower
xTower = 350
yTower = 300
radiusTower = 220
tower = Tower(screen,xTower,yTower,radiusTower)
tower.rotateImages()

def draw_text(display_string, font, surface, x_pos, y_pos):
    text_display = font.render(display_string, 1, (0, 0, 0))
    surface.blit(text_display, (x_pos, y_pos))

def drawScreen():
    global screen
    screen.fill(screenColor)
    screen.blit(space,(0,0))
    screen.blit(topmenu,(0,0))
    screen.blit(botmenu,(0,520))
    screen.blit(path1,(0,0))
    tower.drawImage()

def drawPath():
    for spots in pathPoints:
        pygame.draw.rect(screen,(255,255,255),(spots.x,spots.y,10,10),0)

drawScreen()

# Enemy path
path = []
path.append((10,135))
pathPoints = []
pathPoints.append(pygame.draw.rect(screen,(255,255,255),(10,135,10,10),0))
pathPoints.append(pygame.draw.rect(screen,(255,255,255),(830,615,10,10),0))

main_clock = pygame.time.Clock()

while True:
    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONUP:
            # Create path for enemies
            locX = pygame.mouse.get_pos()[0]
            locY = pygame.mouse.get_pos()[1]
            print(str(locX)+","+str(locY))
            if locX>5 and locX<835 and locY>74 and locY<654:
                path.append((locX,locY))
                pathPoints.append(pygame.draw.rect(screen,(255,255,255),(locX-5,locY-5,10,10),0))

    keys = pygame.key.get_pressed()


    drawScreen()
    drawPath()

    main_clock.tick(50)

    print(path)
    pygame.display.update()