'''
Open CV Framework adapted from Kim Kleiven 112 S17 OpenCVTKinter Demo
'''
import pygame
import cv2
import numpy as np
import math

def findPoints(cnt):
    total = []
    allArrays = []
    if len(cnt) > 0:
        for array in cnt:
            total.append(cv2.arcLength(array, True))
            allArrays.append(array)
        bigIndex = total.index(max(total))
        return cv2.boundingRect(allArrays[bigIndex])
    else:
        return (0,0,0,0)
        
class PygameGame(object):

    def init(self):
        self.cap = cv2.VideoCapture(0)
        self.bgColor = (255, 255, 255)
        
    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        #print("hello",self.paddle_x, self.paddle_y)
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        #return self._keys.get(key, False)
        pass
        
    def processFrame(self):
        cap = self.cap 
        _, frame = cap.read()
        
        frame = cv2.flip( frame, 1 )
        ####BLUE####
        lowerBound = np.array([110,30,50]) #hard-coded to Blue
        upperBound = np.array([130,255,255])#hard-coded to Blue
        
        orange_lowerBound = np.array([5,130,150]) #hard-coded to Orange
        orange_upperBound = np.array([10,200,255])#hard-coded to Orange 
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #hsv value from tutorial
        mask = cv2.inRange(hsv, lowerBound, upperBound)
        
        orange_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        orange_mask = cv2.inRange(hsv, orange_lowerBound, orange_upperBound)
        
        res = cv2.bitwise_and(frame,frame, mask=mask)
        orange_res = cv2.bitwise_and(frame,frame, mask=orange_mask)

        mask = cv2.GaussianBlur(mask,(5,5),10)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        orange_mask = cv2.GaussianBlur(orange_mask,(5,5),10)
        orange_mask = cv2.erode(orange_mask, None, iterations=2)
        orange_mask = cv2.dilate(orange_mask, None, iterations=2)
        
        
        contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)
                                    
        orange_contours, orange_hierarchy = cv2.findContours(orange_mask,
                                        cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
                                    
        x,y,w,h = findPoints(contours)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),5)
        cx = x + w//2
        cy = y + h//2
        area = w*h
        
        ####where I check for swing####
        if len(self.areaList) >= 2:
            self.areaList.pop(0)
        self.areaList.append(area)
        
        if len(self.areaList) == 2 and 0 not in self.areaList:
#addition of .0 ensures real quotient rather than integer truncation bc python2 
            self.paddleAreaRatio = (self.areaList[1]+.0) / (self.areaList[0]+.0)
        #print(self.areaList, self.paddleAreaRatio)
        
        #draw center of bounding box 
        cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
        cv2.putText(frame, "X=%d , Y=%d, area=%d" % (cx, cy, area), 
                    (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                    (255, 255, 255), 2)
                            
        self.rpaddle_x = 205 + (cx*590)/self.webcam_width
        #self.rpaddle_x = self.width//2
        
        x,y,w,h = findPoints(orange_contours)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),5)
        orange_cx = x + w//2
        orange_cy = y + h//2
        cv2.circle(frame, (orange_cx, orange_cy), 7, (255, 255, 255), -1)
        
        cv2.line(frame, (cx, cy), (orange_cx, orange_cy), (255, 255,255), 5)
        
        
        rx, ry = cx, cy
        ox, oy = orange_cx, orange_cy
        opp = (ry - oy)+.0
        adj = (rx - ox)+.0
        if opp == 0 or adj == 0:
            theta = 0
        else: 
            theta = math.degrees(math.atan(opp/adj))
            if rx <= ox and ry >= oy:
                angle = 270 + theta
            elif rx <= ox and ry <= cy:
                angle = 180 - theta
            elif rx >= ox and ry <= cy:
                angle = theta * -1 
            elif rx > cx and ry > cy:
                angle = 360 - theta  
            #print(angle)
            self.paddleAngle = angle
        
        self.frame = frame
        #cv2.imshow('frame', frame)
        #cv2.imshow('mask', res)
        #cv2.imshow('mask2',res+orange_res)
        #cv2.imshow('orange', orange_res)
        #cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('frame', self.webcam_width,self.webcam_height)

    def __init__(self, width=1000, height=650, fps=80, title="MiniPong"):
        self.width = width
        self.height = height
        self.webcam_width = 1275
        self.webcam_height = 720
        self.paddleAreaRatio = 1
        self.fps = fps
        self.title = title
        self.areaList = []
        self.quit = False
        self.swing = False
        self.cameraControl = True
        pygame.init()
        

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            self.processFrame()
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()
