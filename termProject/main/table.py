
import pygame
import math
from GameObject import GameObject

#bounded by points 

class Table(GameObject):
    @staticmethod
    def init():
        Table.tableImage = pygame.image.load('images/table8.png').convert_alpha()
    
    def __init__(self, x, y):
        super(Table, self).__init__(x, y, Table.tableImage, 30)


    def update(self, dt, keysDown, screenWidth, screenHeight):
        #super(Table, self).update(screenWidth, screenHeight)
        #print(self.x, self.y)
        pass


class Splash(GameObject):
    @staticmethod
    def init():
        Splash.splashImage = (pygame.image.load(
                            'images/splash_10.png').convert_alpha())
    
    def __init__(self, x, y):
        super(Splash, self).__init__(x, y, Splash.splashImage, 30)
  
      
        
class Menu(GameObject):
    @staticmethod
    def init():
        Menu.menuImage = pygame.image.load('images/Asset 9.png').convert_alpha()
    
    def __init__(self, x, y):
        super(Menu, self).__init__(x, y, Menu.menuImage, 30)


    


        
    
