
import pygame
import random
import math
from GameObject import GameObject

def distance(x0, y0, x1, y1):
    return((x1+.0-x0+.0)**2 + (y1+.0-y0+.0)**2)**.5
    
def cosineRule(a, b, c):        
     #angle range in radians for rebound
    C = math.acos((a**2 + b**2 - c**2)/(2.0*a*b))
    return C

def ballMotion(self):
    self.y += self.vy
    self.x += self.vx
    
class Ball(GameObject):
    @staticmethod
    def init():
        Ball.ballImage = (pygame.image.load(
                            'images/smallBall.png').convert_alpha())

    def __init__(self, x, y):
        super(Ball, self).__init__(x, y,  Ball.ballImage, 30)
        self.baseSpeed = 15
        self.v = 15
        self.angle = 90
        self.vy = math.sin(math.radians(self.angle)) * self.v
        self.vx = math.cos(math.radians(self.angle)) * self.v
        self.tableCoords = [(345, 120), (655, 120), (795, 520), (205, 520)]
        self.topLeft = self.tableCoords[0]
        self.topRight = self.tableCoords[1]
        self.bottomRight = self.tableCoords[2]
        self.bottomLeft = self.tableCoords[3]
        self.minY = self.tableCoords[0][1]
        self.maxY = self.tableCoords[3][1]


         
        
    def ballInit(self):
        super(Ball, self).__init__(x, y,  Ball.ballImage, 30)
        self.v = 15
        self.angle = 90
        
    def update(self, dt, keysDown, screenWidth, screenHeight, ball, rPaddle, 
                bPaddle):
        super(Ball, self).update(screenWidth, screenHeight)
        #print(self.height, self.width)
        ballMotion(self)
            
        self.vy = math.sin(math.radians(self.angle)) * self.v
        self.vx = math.cos(math.radians(self.angle)) * self.v
        
