import pygame
import math
# inheritance: pygame.sprite.Sprite
class MyHealth():

    def __init__(self, screen, x, y):
        #super().__init__()
        self.screen = screen
        self.image = pygame.image.load("images/myHealthBar33.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.healthList = []
        self.health = 33

    def createHealthBars(self):
        for x in range (1,34):
            num = str(x)
            self.healthList.append(pygame.image.load("images/myHealthBar"+num+".png").convert_alpha())

    def updateHealth(self,num):
        # Don't go out of bounds
        if num > 0:
            if self.health-num > 0:
                self.health -= num
            else:
                self.health = 1
        else:
            if self.health-num <= 33:
                self.health -= num
            else:
                self.health = 33
        self.image = self.healthList[self.health]