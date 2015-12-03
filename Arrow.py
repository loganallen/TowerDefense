#Complete tower code
import pygame
import math

class Arrow(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, angle):
        super(Arrow,self).__init__()
        self.screen = screen
        self.x = x + math.cos(math.radians(angle))*45
        self.y = y - math.sin(math.radians(angle))*45
        self.image = pygame.image.load("images/arrow.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speedDirection = 6
        self.speed = [self.speedDirection,self.speedDirection]
        self.angle = angle

        self.imageList = []

    def rotateImages(self):
        # Create list of 360 rotated bullet images
        initialRotation = 0
        for x in range (0, 360):
            tempImage = pygame.transform.rotate(self.image, initialRotation).convert_alpha()
            initialRotation += 1
            self.imageList.append(tempImage)

    def setDirection(self):
        self.image = self.imageList[self.angle]

    def move(self):
        speed = [self.speedDirection*math.cos(math.radians(self.angle)),-self.speedDirection*math.sin(math.radians(self.angle))]
        self.x += speed[0]
        self.y += speed[1]
        self.rect = self.image.get_rect(center=(self.x,self.y))