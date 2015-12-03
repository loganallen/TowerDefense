#Complete tower code
import pygame
import math

class Bomb(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, angle):
        super(Bomb,self).__init__()
        self.screen = screen
        self.x = x + math.cos(math.radians(angle))*45
        self.y = y - math.sin(math.radians(angle))*45
        self.image = pygame.image.load("images/bomb.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speedDirection = 4
        self.speed = [self.speedDirection,self.speedDirection]
        self.angle = angle

    def move(self):
        speed = [self.speedDirection*math.cos(math.radians(self.angle)),-self.speedDirection*math.sin(math.radians(self.angle))]
        self.x += speed[0]
        self.y += speed[1]
        self.rect = self.image.get_rect(center=(self.x,self.y))


