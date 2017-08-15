
import pygame
import random
from ball import Ball
from GameObject import GameObject


class RedPaddle(GameObject):
    @staticmethod
    def init():
        RedPaddle.rPaddleImage = pygame.transform.rotate(pygame.transform.scale(
                    pygame.image.load('images/straightRP.png').convert_alpha(),
                    (120, 170)), -90)
                    
    def __init__(self, x, y):
        super(RedPaddle, self).__init__(x, y, RedPaddle.rPaddleImage, 30)
        self.x = x

        self.y = y
        self.min_x = 205
        self.max_x = 795
        self.score = 0
        

    def update(self, dt, keysDown, screenWidth, screenHeight, paddle_x, ball, 
                paddleAngle):
        super(RedPaddle, self).update(screenWidth, screenHeight)        
        self.angle = paddleAngle 
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        self.x = paddle_x
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
        
class BluePaddle(GameObject):        
    @staticmethod
    def init():
        BluePaddle.bPaddleImage = pygame.transform.scale(
        pygame.image.load('images/tiltedBPaddle.png').convert_alpha(),
        (160, 160))
        
    def __init__(self, x, y):
        super(BluePaddle, self).__init__(x, y, BluePaddle.bPaddleImage, 30)
        self.x = x
        self.y = y
        self.min_x = 345
        self.max_x = 655
        self.score = 0
        self.speed = 30



    def update(self, dt, keysDown, screenWidth, screenHeight, ball):
        super(BluePaddle, self).update(screenWidth, screenHeight)
        
        #AI movement of oppenent (BLUE) paddle
        
class HowToPaddle(GameObject):        
    @staticmethod
    def init():
        HowToPaddle.howToPaddleImage = pygame.transform.rotate(
                    pygame.image.load('images/howToPaddle.png').convert_alpha(),
                    -90)
        
    def __init__(self, x, y):
        super(HowToPaddle, self).__init__(x, y, HowToPaddle.howToPaddleImage,30)


    def update(self, dt, keysDown, screenWidth, screenHeight, paddleAngle):
        self.angle = paddleAngle 
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
        
class Arrow(GameObject):
    @staticmethod
    def init():
        Arrow.arrowImage = pygame.image.load('images/arrow.png').convert_alpha()
    
    def __init__(self, x, y):
        super(Arrow, self).__init__(x, y, Arrow.arrowImage, 30)

 
