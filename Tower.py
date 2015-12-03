#Complete tower code
import pygame
import math
from MyHealth import MyHealth
# For inheritance with sprites: pygame.sprite.Sprite
class Tower():

    def __init__(self, screen, x, y, radius, number):
        #super().__init__()
        self.radius = radius
        self.x = x
        self.y = y
        self.number = number
        self.screen = screen

        if number==1:
            self.image = pygame.image.load("images/Tower.png").convert_alpha()
        else:
            self.image = pygame.image.load("images/Tower2.png").convert_alpha()

        self.rect = self.image.get_rect(center=(x, y))
        self.range = (self.rect.center, (radius,radius))
        self.rangeColor = (255,255,100)
        self.circleRange = pygame.draw.circle((screen), self.rangeColor, (x,y), radius, 2)

        self.imageList = []
        self.angle = 0

        if number == 1:
            self.health = MyHealth(screen,775,20)
            self.health.createHealthBars()


    def rotateImages(self):
        # Create list of 360 rotated images
        initialRotation = 0
        for x in range (0, 360):
            tempImage = pygame.transform.rotate(self.image, initialRotation).convert_alpha()
            initialRotation += 1
            self.imageList.append(tempImage)

    def updateAngle(self,mouseX,mouseY):
        # Update angle that tower points towards
        radians = -math.atan2(mouseY-self.y,mouseX-self.x)
        degrees = math.floor(math.degrees(radians))
        #print(degrees)
        self.angle = int(degrees)
        self.image = self.imageList[int(degrees)]

    def drawImage(self,xx,yy):
        self.x = xx
        self.y = yy
        pygame.draw.circle((self.screen), self.rangeColor, (self.x,self.y), self.radius, 2)
        self.image = self.imageList[self.angle]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.screen.blit(self.image,self.rect.topleft)

    def drawHealth(self):
        if self.number == 1:
            self.screen.blit(self.health.image,self.health.rect.topleft)

    def updateRadius(self,rad):
        self.radius += rad

    def hurt(self,damage):
        self.health.updateHealth(damage)
