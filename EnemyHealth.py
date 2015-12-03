import pygame
import math

class EnemyHealth(pygame.sprite.Sprite):

    def __init__(self, screen, x, y):
        super(EnemyHealth, self).__init__()
        self.screen = screen
        self.image = pygame.image.load("images/healthBar15.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y-20))

        self.healthList = []
        self.health = 15

    def createHealthBars(self):
        for x in range (0,16):
            num = str(x)
            self.healthList.append(pygame.image.load("images/healthBar"+num+".png").convert_alpha())

    def updateHealth(self,num):
        if self.health-num >= 0:
            self.health -= num
        else:
            self.health = 0
        self.image = self.healthList[int(self.health)]
        #print("Health: "+str(self.health))

    def move(self,x,y):
        self.rect = self.image.get_rect(center=(x, y-20))
