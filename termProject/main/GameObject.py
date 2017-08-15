'''

implements the base GameObject class, which defines the vanishing perspective 
for game paddles and ball
'''
import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image, self.radius = x, y, image, radius
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()
        self.updateRect()
        self.velocity = (0, 0)
        self.angle = 0
        
    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, screenWidth, screenHeight):
        self.ratio = (31.0/59.0) + (self.y+.0)/(screenHeight+.0)
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        w,h = self.image.get_size()
        #ensures vanishing perspective 
        self.image = pygame.transform.scale(self.baseImage, (int(w*self.ratio), 
        int(h*self.ratio)))
        self.w,self.h = self.image.get_size()
        self.updateRect()

