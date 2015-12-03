import pygame
import math
from EnemyHealth import EnemyHealth

class Enemy(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, monsterType):
        super(Enemy, self).__init__()
        self.screen = screen
        self.x = x
        self.initX = x
        self.initY = y
        self.y = y
        self.inflictDamage = False
        self.destinationPoint = 0
        self.health = EnemyHealth(screen,x,y)
        self.health.createHealthBars()
        self.alive = True

        if monsterType == 1:
            self.image = pygame.image.load("images/monster1.png").convert_alpha()
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = [.8,.8]
            self.damage = 1
            self.value = 5
            self.defense = 1
        elif monsterType == 2:
            self.image = pygame.image.load("images/monster2.png").convert_alpha()
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = [.9,.9]
            self.damage = 2
            self.value = 10
            self.defense = 1.25
        elif monsterType == 3:
            self.image = pygame.image.load("images/monster3.png").convert_alpha()
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = [1,1]
            self.damage = 3
            self.value = 15
            self.defense = 1.5
        elif monsterType == 4:
            self.image = pygame.image.load("images/monster11.png").convert_alpha()
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = [1.3,1.3]
            self.damage = 4
            self.value = 20
            self.defense = 1.75
        elif monsterType == 5:
            self.image = pygame.image.load("images/monster12.png").convert_alpha()
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = [1.4,1.4]
            self.damage = 5
            self.value = 25
            self.defense = 2
        elif monsterType == 6:
            self.image = pygame.image.load("images/monster13.png").convert_alpha()
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = [1.5,1.5]
            self.damage = 6
            self.value = 30
            self.defense = 2.25

        self.monsterType = monsterType-1

    def hit(self,damage):
        self.health.updateHealth(damage/self.defense)

    def checkReachPoint(self):
        if self.rect.colliderect(pygame.Rect(self.xDest,self.yDest,5,5)):
            self.updateDestination()

    def setPath(self,path):
        self.path = path
        self.xDest = self.path[self.destinationPoint][0]
        self.yDest = self.path[self.destinationPoint][1]

    def updateDestination(self):
        if self.destinationPoint < len(self.path)-1:
            self.destinationPoint += 1
        else:
            self.inflictDamage = True
            self.alive = False

        self.xDest = self.path[self.destinationPoint][0]
        self.yDest = self.path[self.destinationPoint][1]
        vector = pygame.math.Vector2((self.xDest-self.x),(self.yDest-self.y))

    def move(self):
        if self.health.health == 0:
            self.alive = False

        if self.alive:
            if self.x < self.xDest:
                self.x += self.speed[0]
            if self.x > self.xDest:
                self.x -= self.speed[0]
            if self.y < self.yDest:
                self.y += self.speed[1]
            if self.y > self.yDest:
                self.y -= self.speed[1]

        self.health.move(self.x,self.y)
        self.rect = self.image.get_rect(center=(self.x, self.y))
