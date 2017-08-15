'''
pygame Framework Adapted from: 
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
import cv2
import pygame
from table import Table, Splash, Menu
from paddles import BluePaddle, RedPaddle, HowToPaddle, Arrow
from ball import Ball
from pygameopencv import PygameGame
import random
import math
import numpy 

def distance(x0, y0,  x1, y1):
    return((x1+.0-x0+.0)**2 + (y1+.0-y0+.0)**2)**.5
     
def cosineRule(a, b, c):     
    #angle range in radians for rebound   
    C = math.acos((a**2 + b**2 - c**2)/(2.0*a*b)) 
    return C
       
def checkForSwing(self):
    #print(self.ratio)
    if self.paddleAreaRatio > 1.5:
        self.swing = True
    else: self.swing = False

class Game(PygameGame):
    def init(self):
        pygame.font.init()
        self.bgColor = (255, 255, 255)
        self.cap = cv2.VideoCapture(0)
        self.difficulty = "easy"
        self.rpaddle_x = self.width//2
        self.rpaddle_y = 650 - 150
        self.bpaddle_x = self.width // 2
        self.bpaddle_y = 75
        self.ball_x = 500
        self.ball_y = 300
        self.swing = False
        self.tableCoords = [(345, 120), (655, 120), (795, 520), (205, 520)]
        self.boundCoords = [(285, 120), (715, 120), (855, 520), (145, 520)]
        self.topLeft = self.boundCoords[0]
        self.topRight = self.boundCoords[1]
        self.bottomRight = self.boundCoords[2]
        self.bottomLeft = self.boundCoords[3]
        self.minY = self.boundCoords[0][1]  - 40
        self.maxY = self.boundCoords[3][1] + 40
        slope1 =  ((self.topLeft[1]+.0-self.bottomLeft[1]+.0)/
                    (self.topLeft[0]+.0-self.bottomLeft[0]+.0))
        self.f1 = (str(slope1)+"*(%d-"+str(self.topLeft[0]+.0)+")+"+
                    str(self.topLeft[1]+.0))
        slope2 = ((self.topRight[1]+.0-self.bottomRight[1]+.0)/
                    (self.topRight[0]+.0-self.bottomRight[0]+.0))
        self.f2 = (str(slope2)+"*(%d-"+str(self.topRight[0]+.0)+")+"+
                    str(self.topRight[1]+.0))
        self.leftBound = -(20.0/7.0), 'x', (6540.0/7.0)
        self.rightBound = (20.0/7.0), 'x', (-13460.0/7.0)
        self.isPaused = False
        self.min_x = 345
        self.max_x = 655 
        self.displayErrorBox = False
        self.angle = 90
        self.guideLine = None
        
        self.gameInit()
        
        
        ##Button Locations
        self.help = (128, 655)
        self.home = (186, 657)
        self.play = (815, 655)
        self.pause = (868, 655)
        self.buttonR = 20
        
        self.player1Score = 0
        self.player2Score = 0
        
        self.lastPlayer = None 
        self.net = ((309, 226),(689, 227))
        
        self.mode = "home"
        self.helpScreen = False
        
        self.viewCV = False
        #Messages
        self.message = '' 

        Menu.init()
        menuImage = Menu(self.width // 2, 175)
        self.menuGroup = pygame.sprite.GroupSingle(menuImage)

        Table.init()
        table = Table(self.width // 2, 325)
        self.tableGroup = pygame.sprite.GroupSingle(table)
        
        Splash.init()
        splash = Splash(self.width // 2, self.height-30)
        self.splashGroup = pygame.sprite.GroupSingle(splash)
        
        HowToPaddle.init()
        howToPaddle = HowToPaddle(self.width//2, self.height//2-50)
        self.howToPaddleGroup = pygame.sprite.GroupSingle(howToPaddle)
        
        Arrow.init()
        arrow = Arrow(self.width//2, self.height//2-50)
        self.arrowGroup = pygame.sprite.GroupSingle(arrow)

    def gameInit(self):
        self.paddleAngle = 270
        self.gameStarted = False
        self.rpaddle_x = self.width//2
        self.rpaddle_y = 650 - 150
        self.bpaddle_x = self.width // 2
        self.bpaddle_y = 75
        self.ball_x = self.width//2
        self.ball_y = 300

        self.player1Score = 0
        self.player2Score = 0
        self.winningPlayer = ""
        self.gameWon = False
        
        self.lastPlayer = None
         
        BluePaddle.init()
        bPaddle = BluePaddle(self.bpaddle_x, self.bpaddle_y)
        self.bPaddleGroup = pygame.sprite.GroupSingle(bPaddle)

        RedPaddle.init()
        rPaddle = RedPaddle(self.rpaddle_x, self.rpaddle_y)
        self.rPaddleGroup = pygame.sprite.GroupSingle(rPaddle)

        Ball.init()
        ball = Ball(self.ball_x, self.ball_y)
        self.ballGroup = pygame.sprite.GroupSingle(ball)
        
######################################################################     
# MODE DISPATCHER
###################################################################### 
        
    def keyPressed(self, code, mod):  
        if self.mode == "game": self.gameKeyPressed(code, mod)
        if self.mode == "home": self.homeKeyPressed(code, mod)
        if self.mode == "howTo": self.howToKeyPressed(code, mod)
        if self.mode == "options": self.optionsKeyPressed(code, mod)
        
    def mousePressed(self, x, y):
        print(x, y)
        if self.mode == "game": self.gameMousePressed(x, y)
        if self.mode == "home": self.homeMousePressed(x, y)
        if self.mode == "howTo": self.howToMousePressed(x, y)
        if self.mode == "options": self.optionsMousePressed(x, y)
        
    def timerFired(self, screen):
        if self.viewCV:
            cv2.imshow('Camera Controls', self.frame)
        if self.mode == "game": self.gameTimerFired(screen)
        if self.mode == "home": self.homeTimerFired(screen)
        if self.mode == "howTo": self.howToTimerFired(screen)
        if self.mode == "options": self.optionsTimerFired(screen)
           
    def redrawAll(self, screen):
        if self.mode == "game": self.gameRedrawAll(screen)
        if self.mode == "home": self.homeRedrawAll(screen)
        if self.mode == "howTo": self.howToRedrawAll(screen)
        if self.mode == "options": self.optionsRedrawAll(screen)
        
######################################################################     
# HOME MODE
###################################################################### 
                
    def homeKeyPressed(self, code, mod):
        if code == pygame.K_SPACE:
            pass
        
    def homeMousePressed(self, x, y):
        #print(x, y)
        if (x > 325) and (x < 675) and (y > 375) and (y < 445):
            self.mode = "game"
            self.gameStarted = True
            
        elif (x > 325) and (x < 675) and (y > 475) and (y < 545):
            self.mode = "howTo"
            
        elif (x > 325) and (x < 675) and (y > 575) and (y < 645):
            self.mode = "options"
            self.lastMode = "home"
            

    def homeTimerFired(self, screen):
        pass
        
    def drawButton(self, screen, cx, cy):
        lightGrey = (242, 242, 242)
        darkerGrey = (232, 232, 232)
        
        width = 350
        height = 75
        
        x0, y0, w, h = cx - width//2, cy - width//2, width, height
        dims = (x0, y0, w, h)
        pygame.draw.rect(screen, darkerGrey, dims, 0)
        
        width = 340
        height = 65
        x0, y0, w, h = cx - width//2, cy - width//2, width, height
        dims = (x0, y0, w, h)
        pygame.draw.rect(screen, lightGrey, dims, 0)
        
    def renderText(self, screen, text, size, cx, cy, color = (0,0,0)):
        font = pygame.font.SysFont("verdana", size)
        
        font.set_bold(True)
        text = font.render(text, True, (0, 0, 0), None)
        Text = text.get_rect()
        Text.centerx = cx 
        Text.centery = cy
        
        screen.blit(text, Text)
    
    def drawMenu(self, screen):        
        marginY = 40
        marginX = 250
        border = 10
        
        self.drawButton(screen, self.width//2, 550)
        self.drawButton(screen, self.width//2, 650)
        self.drawButton(screen, self.width//2, 750)
        if self.gameStarted == True: text = "Continue Playing"
        else: text = 'Play Game'
        self.renderText(screen, text, 25, self.width//2, 410)
        self.renderText(screen, 'How To Play', 25, self.width//2, 510)
        self.renderText(screen, 'Options', 25, self.width//2, 610)
        
    def homeRedrawAll(self, screen):
        self.drawMenu(screen)
        self.menuGroup.draw(screen)
        
######################################################################     
# HOW-TO MODE
###################################################################### 

    def howToKeyPressed(self, code, mod):
        pass
        
    def howToMousePressed(self, x, y):
        if (x > 50) and (x < 150) and (y > 25) and (y < 100):
            self.mode = "home"
        
    def howToTimerFired(self, dt):
         howToPaddle = self.howToPaddleGroup.sprite
         
         self.howToPaddleGroup.update(dt, self.isKeyPressed, self.width, 
                                        self.height, self.paddleAngle) 
         howToPaddle = self.howToPaddleGroup.sprite
         checkForSwing(self)        
         if self.swing: 
             w,h = howToPaddle.image.get_size()
             howToPaddle.image = pygame.transform.scale(howToPaddle.image, 
                                (int(w*.95), int(h*.95))) 
             howToPaddle.image = pygame.transform.scale(howToPaddle.image, 
                                (int(w*.9), int(h*.9))) 
    def howToRedrawAll(self, screen):
        self.drawHelpButton(screen, 100, 50, 100, 50)
        self.renderText(screen, "exit", 15, 100, 50)
        
        self.arrowGroup.draw(screen)
        self.howToPaddleGroup.draw(screen)
        
        self.renderText(screen, "Hold paddle with blue face showing towards", 
                        25, self.width//2, self.height//2+200)
        self.renderText(screen, 
                        "the screen and orange end visible to the camera.", 25, 
                        self.width//2, self.height//2+250)
        self.renderText(screen, 
                        "Swing Paddle towards the screen to hit the ball!", 25, 
                        self.width//2, self.height//2+300)
######################################################################     
# OPTIONS MODE
######################################################################     
    def optionsKeyPressed(self, code, mod):
        pass
    
    def optionsMousePressed(self, x, y):
        if (x > 50) and (x < 150) and (y > 25) and (y < 100):
            self.mode = self.lastMode
        elif self.displayErrorBox == True:
            if y > 365 and y < 395:
                if x > 430 and x < 490:
                    self.gameInit()
                    self.mode = 'options'
                    self.difficulty = self.tempSelected
                    self.displayErrorBox = False
                elif x > 510 and x < 570:
                    self.displayErrorBox = False
        elif x > self.width//2-125 and x < self.width//2+125:
            if (y > 315) and (y < 385):
                if self.gameStarted == False:
                    self.difficulty = "easy"
                elif self.gameStarted == True and self.difficulty != 'easy':
                    self.displayErrorBox = True
                    self.tempSelected = "easy"
            elif (y > 415) and (y < 485):
                if self.gameStarted == False:
                    self.difficulty = "medium"
                elif self.gameStarted == True and self.difficulty != 'medium':
                    self.displayErrorBox = True
                    self.tempSelected = "medium"
            elif (y > 515) and (y < 585):
                if self.gameStarted == False:
                    self.difficulty = "hard"
                elif self.gameStarted == True and self.difficulty != 'hard':
                    self.displayErrorBox = True
                    self.tempSelected = "hard"
            elif (y > 615) and (y < 685):
                self.viewCV = True
             
    def optionsTimerFired(self, screen):
        pass
            
    def drawHelpButton(self,screen,cx,cy,width,height, color =(242, 242, 242)):
        light = color
        darker = (color[0]-10, color[1]-10, color[2]-10)
        margin=10
        
        x0, y0, w, h = cx - width//2, cy - height//2, width, height
        dims = (x0, y0, w, h)
        pygame.draw.rect(screen, darker, dims, 0)
        
        width = width-margin
        height = height-margin
        
        x0, y0, w, h = cx - width//2, cy - height//2, width, height
        dims = (x0, y0, w, h)
        pygame.draw.rect(screen, light, dims, 0)  
                  
    def drawButtons(self, screen):
        GREEN = (150, 216, 143)
        YELLOW = (247, 247, 148)
        RED = (247, 141, 137)
        
        if self.difficulty == "easy":
            self.drawHelpButton(screen, self.width//2, self.height//2, 250, 75, 
                                GREEN)
        else: self.drawHelpButton(screen, self.width//2, self.height//2, 250,75)
      
        if self.difficulty == "medium":  
            self.drawHelpButton(screen, self.width//2, self.height//2+100, 250, 
                                75, YELLOW)
        else: self.drawHelpButton(screen, self.width//2, self.height//2+100,250, 
                                    75)
        
        if self.difficulty == "hard":
            self.drawHelpButton(screen, self.width//2, self.height//2+200, 250, 
                                75, RED)
        else: self.drawHelpButton(screen, self.width//2, self.height//2+200, 
                                250, 75)
        
        if self.viewCV == True:
            self.drawHelpButton(screen, self.width//2, self.height//2+300, 250, 
                                75, (222, 222, 222))
        else: self.drawHelpButton(screen, self.width//2, self.height//2+300,250, 
                                75)
    
        self.drawHelpButton(screen, 100, 50, 100, 50)
        
        self.renderText(screen, "Difficulty Settings", 35, self.width//2, 
                        self.height//2-160)
        self.renderText(screen, "Easy", 20, self.width//2, self.height//2)
        self.renderText(screen, "Medium", 20, self.width//2, self.height//2+100)
        self.renderText(screen, "Hard", 20, self.width//2, self.height//2+200)
        self.renderText(screen, "Show Video Capture", 15, self.width//2, 
                        self.height//2+300)
        self.renderText(screen, "exit", 15, 100, 50)
        
        if self.displayErrorBox == True:
            self.drawHelpButton(screen, self.width//2, self.height//2, 350, 150)
            self.drawHelpButton(screen, self.width//2-40, self.height//2+30, 60, 
                                30, GREEN)
            self.drawHelpButton(screen, self.width//2+40, self.height//2+30, 60, 
                                30, RED)
        
            self.renderText(screen, "Changing difficulty settings", 15, 
                            self.width//2, self.height//2-40)
            self.renderText(screen, "will start a new game. Continue?", 15, 
                            self.width//2, self.height//2-20)
            self.renderText(screen, "yes", 12, self.width//2-40, 
                            self.height//2+30)
            self.renderText(screen, "no", 12, self.width//2+40, 
                            self.height//2+30)
        
        
    def optionsRedrawAll(self, screen):
        self.drawButtons(screen)      
             
######################################################################     
# GAME MODE
######################################################################
    def movePaddle(self, paddle, ball, speed):
        if paddle.x > ball.x:
            if abs(paddle.x - ball.x) < speed:
                paddle.x -= 1
            else: paddle.x -= speed
        elif paddle.x < ball.x:
            if abs(paddle.x - ball.x) < speed:
                paddle.x += 1
            else: paddle.x += speed

    #### simple "AI" component ###
    ### Oponent paddle tracks ball ###
    def paddleTracking(self, bPaddle, ball, trackingSpeed, hitSpeed, accuracy): 
        #if self.ballHitsPaddle(ball, bPaddle):
        if pygame.sprite.collide_rect(ball, bPaddle):
            w,h = bPaddle.image.get_size() 
            bPaddle.image = pygame.transform.scale(bPaddle.image, (int(w*1.2), 
                                                    int(h*1.2)))
            p = random.randint(0, 20)
            if accuracy == 1:
                if p <= 2:
                    self.reboundAngleBlue(ball)
            elif accuracy == 2:
                if p <= 15:
                    self.reboundAngleBlue(ball)
            elif accuracy == 3:
                self.reboundAngleBlue(ball)
            self.lastPlayer = "Blue"
            ball.v = hitSpeed
        if ball.x != bPaddle.x:
            self.movePaddle(bPaddle, ball, trackingSpeed)
            
    def AI(self, bPaddle, ball):
        if self.difficulty == 'easy':
            trackingSpeed = 5
            hitSpeed = 10
            accuracy = 1
        if self.difficulty == 'medium':
            trackingSpeed = 15
            hitSpeed = 20
            accuracy = 2
        elif self.difficulty == 'hard':
            trackingSpeed = 30
            hitSpeed = 35
            accuracy = 3
        self.paddleTracking(bPaddle, ball, trackingSpeed, hitSpeed, accuracy)

             
    def reboundAngleRed(self, ball):
        destination = (random.randint(self.topLeft[0], self.topRight[0]), 
                        self.topRight[1])
        destX, destY = destination
        a = distance(self.bottomRight[0],self.bottomRight[1], ball.x, ball.y)
        b = distance(destX, destY, ball.x, ball.y)
        c = distance(destX, destY, self.bottomRight[0],self.bottomRight[1])
        #print(a, b, c)
        C = math.degrees(cosineRule(a, b, c)) 
        self.guideLine = (destX, destY, ball.x, ball.y)
        ball.angle = (180 - C) + 180
        #print('heeeeeere')
        
        
    def reboundAngleBlue(self, ball):
        destination = (random.randint(self.bottomLeft[0], self.bottomRight[0]), 
                        self.bottomRight[1])
        destX, destY = destination
        a = distance(self.topRight[0], self.topRight[1], ball.x, ball.y)
        b = distance(destX, destY, ball.x, ball.y)
        c = distance(self.topRight[0], self.topRight[1], destX, destY)
        #print(a, b, c)
        C = math.degrees(cosineRule(a, b, c)) 
        #print(C)
        ball.angle = C
        
        #self.guideLine = (destX, destY, ball.x, ball.y)
        self.guideline = None
    def ballHitsPaddle(self, ball, paddle):
        #w, h = paddle.get_image_size()
        if paddle.y < 200:
            if ((ball.y <= paddle.y) and 
                (ball.x < paddle.x+20) and 
                (ball.x > paddle.x-20)):
                return True
        elif paddle.y > 200:
            if ((ball.y >= paddle.y) and 
                (ball.x < paddle.x+20) and 
                (ball.x > paddle.x-20)):
                return True
            
    def ballGoingTowardsBlue(self,ball):
        return(ball.angle > 180 and ball.angle < 360)
    
    def ballGoingTowardsRed(self, ball):
         return(ball.angle > 0 and ball.angle < 180)
        
    def ballOffTable(self, ball):
        line1 = self.f2 % (ball.x+.0)
        line2 = self.f1 % (ball.x+.0)
        lineY1 = eval(line1)
        lineY2 = eval(line2)
        
        if ball.y > self.maxY:
            return True
        elif ball.y < self.minY:
            return True
        elif ball.x <= self.topLeft[0] and ball.y < lineY1:
            return True   
        elif ball.x >= self.topRight[0] and ball.y < lineY2:
            return True
        return False 
        
    def ballOnTable(self, ball):
        line1 = self.f2 % (ball.x)
        line2 = self.f1 % (ball.x)
        lineY1 = eval(line1)
        lineY2 = eval(line2) 
        d =150
        
        if ball.y < self.minY - d or ball.y > ball.maxY + d:
            return False

        return(ball.y+ball.vy > lineY1 + d and ball.y+ball.vy > lineY2 + d)
        
    def checkForPoint(self,ball):
        if self.ballGoingTowardsBlue:
            if ball.y < 0:
                self.player1Score += 1
                return True
            elif abs(ball.y - 250) <= ball.vy:
                if ball.x < 290 or ball.x > 710:
                    self.player2Score += 1
                    return True
        else:
            if ball.y > 600:
                self.player2Score+= 1
                return True
            elif abs(ball.y - 250) <= ball.vy:
                if ball.x < 290 or ball.x > 710:
                    self.player1Score += 1
                    return True
        return False
         
    def restartBall(self, ball):
        Ball.init()
        ball = Ball(self.ball_x, self.ball_y)
        self.ballGroup = pygame.sprite.GroupSingle(ball)
        
    def checkForWin(self):
        if self.player1Score >= 7 or self.player2Score >= 7:
            winningScore = max(self.player1Score, self.player2Score)
            if winningScore == self.player1Score:
                self.winningPlayer = "Player 1"
            elif winningScore == self.player2Score:
                self.winningPlayer = "Player 2" 
            self.gameWon = True
       
                           
    def gameMousePressed(self, x, y):
        buttonList = [self.help, self.home, self.play, self.pause]
        
        for button in buttonList:
            buttonX, buttonY = button
            if distance(x, y, buttonX, buttonY) <= self.buttonR:
                if button == self.help:
                    self.mode = 'options'
                    self.lastMode = 'game'
                elif button == self.home:
                    self.mode = "home"
                elif button == self.play:
                    self.isPaused = False
                elif button == self.pause:
                    self.isPaused = True
                    self.message = "Paused"
                    
    def gameKeyPressed(self, code, mod):            
        
        if code == pygame.K_SPACE:
            #print("PAUSED")
            self.isPaused = not self.isPaused
            self.message = "Paused"
        elif code == pygame.K_LEFT:
            self.player2Score += 1  
        elif code == pygame.K_RIGHT:
            self.player1Score += 1  
        elif code == 114:###"r"####
            if self.gameWon == True:
                self.gameInit()
            else:
                Ball.init()
                ball = Ball(self.ball_x, self.ball_y)
                self.ballGroup = pygame.sprite.GroupSingle(ball)

    def gameTimerFired(self, dt):
        ball = self.ballGroup.sprite
        rPaddle = self.rPaddleGroup.sprite
        bPaddle = self.bPaddleGroup.sprite
        
        if self.isPaused == True or self.gameWon == True: return 
        self.rPaddleGroup.update(dt, self.isKeyPressed, self.width, self.height, 
                                self.rpaddle_x, ball, self.paddleAngle) 
        self.bPaddleGroup.update(dt, self.isKeyPressed, self.width, self.height, 
                                ball)
        self.ballGroup.update(dt, self.isKeyPressed, self.width, self.height,
                                ball, rPaddle, bPaddle)
        #print("yababa", self.ball_x, self.bpaddle_x, self.rpaddle_x)
    
        if self.ballGoingTowardsBlue: #ball is traveling towards blue paddle
            self.AI(bPaddle, ball)
        
        if pygame.sprite.collide_rect(ball, rPaddle):
            if self.swing == True: 
                self.reboundAngleRed(ball)
                ball.v  = (15 * self.paddleAreaRatio)
                self.lastPlayer = "Red"
                
        if ball.y > 600:
            self.restartBall(ball)
            self.player2Score += 1
            
        if self.checkForPoint(ball) == True:
            self.restartBall(ball)
        
        checkForSwing(self)        
        print(self.paddleAreaRatio, self.swing)
    
        if self.isPaused == True:
            self.message = "Paused"
        else: self.message = None
        #print(self.message)
        
        if self.helpScreen == True:
            self.displayHelpScreen(screen)
        self.checkForWin()
        
    def displayHelpScreen(screen):
        self.drawHelpScreen(screen)
        
    def drawHelpScreen(screen):
        pass
###Using code modified from:
#codereview.stackexchange.com/questions/70143/drawing-a-dashed-line-with-pygame 
    def drawDottedLine(self, screen, start_pos, end_pos, color=(255, 255, 255),
                        width=3, dash_length=5):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dl = dash_length
    
        if (x1 == x2):
            ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
            xcoords = [x1] * len(ycoords)
        elif (y1 == y2):
            xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
            ycoords = [y1] * len(xcoords)
        else:
            a = abs(x2 - x1)
            b = abs(y2 - y1)
            c = round(math.sqrt(a**2 + b**2))
            dx = dl * a / c
            dy = dl * b / c
    
            xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
            ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]
    
        next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
        last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
        for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
            start = (round(x1), round(y1))
            end = (round(x2), round(y2))
            #pygame.draw.line(screen, color, start, end, width)
            pygame.draw.circle(screen, (255, 255, 255), (int(x1), int(y1)), 2, 0)
            
    def drawSplashBoard(self, screen):    
        self.renderText(screen, str(self.player2Score), 25, self.width // 2 - 75, self.height - 40)
        self.renderText(screen, str(self.player1Score), 25, self.width // 2 + 75, self.height - 40)
        
    def drawMessageBox(self, screen, message):        
        self.renderText(screen, message, 50, self.width//2, self.height//2-100, (255,255,255))
        #self.renderText(screen, message, 50, self.width//2, self.height//2-100)
     
    def gameRedrawAll(self, screen):
        self.tableGroup.draw(screen)
        self.bPaddleGroup.draw(screen)
        self.ballGroup.draw(screen)
        self.rPaddleGroup.draw(screen)
        self.splashGroup.draw(screen)
        self.drawSplashBoard(screen)
            
   
        if self.guideLine != None:
            start_pos = (self.guideLine[0], self.guideLine[1])
            end_pos = (self.guideLine[2], self.guideLine[3])
            self.drawDottedLine(screen, start_pos, end_pos)
            
        if self.isPaused:
            self.drawMessageBox(screen, self.message)
        

        if self.winningPlayer != "":
            text = "%s Wins!" % self.winningPlayer
            self.renderText(screen, text, 40, self.width//2, self.height//2-100, 
                            (255,255,255))
            self.renderText(screen, "press 'r' to play again", 25,self.width//2, 
                            self.height//2, (255,255,255))

Game(1000, 700).run()
