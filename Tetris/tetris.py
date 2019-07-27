#########################################
# Programmer: Hayden Wolff
# Date: 04/7/2019
# File Name: tetris.py
#########################################
#############
## Imports ##
#############
from tetris_classes import *
from random import randint
import time
import pygame
import sys
pygame.init()


HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))

#############
## Colours ##
#############

GREY = (192,192,192)
black = (0,0,0)
green = (0,255,0)
blue = (0,100,255)
white = (255,255,255)
red = (255,0,0)

##########################
## POSITIONS FOR BLOCKS ##
##########################

#---------------------------------------#
COLUMNS = 14                            #
ROWS = 22                               # 
LEFT = 1                                # 
RIGHT = LEFT + COLUMNS                  # 
MIDDLE = LEFT + COLUMNS//2              #
TOP = -1                                #
FLOOR = TOP + ROWS                      #
#---------------------------------------#

###############################################
## Calling Classes and Variables for Classes ##
###############################################
delay = 100
score = 0
level = 1
score = 0
timer = 0
shapeNo2 = randint(1,7)
shapeNo = randint(1,7)
holdShapeNo = 0
inPlay = False
doubleTetris = False
currentHold = False
paused = False
introS = True
endS = False
rulesS = False
shape = Shape(MIDDLE,TOP+2,shapeNo)
nextShape = Shape(MIDDLE+11,TOP+10,shapeNo2)
shadow = Shape(MIDDLE,TOP+2,shapeNo)
floor = Floor(LEFT,FLOOR,COLUMNS)
roof = Floor(LEFT,TOP+1,COLUMNS)
leftWall = Wall(LEFT,0,ROWS)
rightWall = Wall(RIGHT,0,ROWS)
obstacle = Obstacles(LEFT, FLOOR)
scoring = Score(score,doubleTetris,level,delay)

#############
## Images  ##
#############

introScreen = pygame.image.load("Tetris Background (1).png")
introScreen = pygame.transform.scale(introScreen,(WIDTH,HEIGHT))

endScreen = pygame.image.load("Tetris-Game-Over.jpg")
endScreen = pygame.transform.scale(endScreen,(WIDTH,HEIGHT))

background = pygame.image.load("Tetris-Game-Background(1).jpg")
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

#############
## Sounds  ##
#############

land = pygame.mixer.Sound("Ttrs - Land.wav")
land.set_volume(0.8)
music = pygame.mixer.Sound("Ttrs - GB A-Type Music.wav")
music.set_volume(0.09)
lineClear = pygame.mixer.Sound("Ttrs - Clear Line.wav")
lineClear.set_volume(0.8)
tetrisClear = pygame.mixer.Sound("Ttrs - Tetris.wav")
tetrisClear.set_volume(0.8)
tetrisIntro = pygame.mixer.Sound("Ttrs - GB Intro.wav")
tetrisIntro.set_volume(0.09)
tetrisGameOver = pygame.mixer.Sound("Ttrs - GB Game Over.wav")
tetrisGameOver.set_volume(0.09)


####################
## Fonts and Text ##
####################

myFont = pygame.font.SysFont("Arial Black", 30)
myFont2 = pygame.font.SysFont("Arial Black", 15)
myFont3 = pygame.font.SysFont("Arial Black", 13)
play = myFont.render("PLAY",1,black)
rules = myFont.render("RULES",1,black)



#---------------------------------------#
#   functions                           #
#---------------------------------------#
def redraw_screen():
    screen.blit(background,(0,0))                                         # This Function draws the main part of the game
    levels = "Level: "+str(level)                                         # It draws all the shapes, The shadow, the next shape, 
    time = myFont.render("Time: "+str(round((timer),0)),1,WHITE)          # The boxes that they are in, and the text that are drawn
    scores = myFont.render("Score: "+str(score),1,WHITE)                  # This function also draws the boxes to match with the shape
    levels = myFont.render(levels,1,WHITE)                                # So the shape is centred in the box
    screen.blit(time,(425,500))
    screen.blit(scores,(425,50))
    screen.blit(levels,(425,275))
    shadow.fill(screen, GRIDSIZE)
    shape.drawImages(screen, GRIDSIZE)
    nextShape.drawImages(screen, GRIDSIZE)
    if currentHold and holdShapeNo != 0:
        holdShape.drawImages(screen, GRIDSIZE)
    floor.draw(screen, GRIDSIZE)
    leftWall.draw(screen, GRIDSIZE)
    rightWall.draw(screen, GRIDSIZE)
    obstacle.drawImages(screen, GRIDSIZE)
    if shapeNo2 == 7:
        nextText = myFont3.render("NEXT SHAPE",1,WHITE)
        screen.blit(nextText,(430,155))
        pygame.draw.rect(screen,white,(425,175,100,100),1)
    elif shapeNo2 == 5:
        nextText = myFont2.render("NEXT SHAPE",1,WHITE)
        screen.blit(nextText,(447,180))
        pygame.draw.rect(screen,white,(425,200,150,75),1)
    else:
        nextText = myFont2.render("NEXT SHAPE",1,WHITE)
        screen.blit(nextText,(433,155))
        pygame.draw.rect(screen,white,(425,175,125,100),1)
    if holdShapeNo == 7:
        holdText = myFont3.render("ON HOLD",1,WHITE)
        screen.blit(holdText,(667,155))
        pygame.draw.rect(screen,white,(650,175,100,100),1)
    elif holdShapeNo == 5:
        holdText = myFont2.render("ON HOLD",1,WHITE)
        screen.blit(holdText,(660,180))
        pygame.draw.rect(screen,white,(625,200,150,75),1)
    else:
        holdText = myFont2.render("ON HOLD",1,WHITE)
        screen.blit(holdText,(673,155))
        pygame.draw.rect(screen,white,(650,175,125,100),1)
    pygame.display.update()

def intro_screen():
    screen.blit(introScreen,(0,0))          # This function draws the intro screen and
    playRect = pygame.Surface((250,75))     # the Two boxes, rules and play
    rulesRect = pygame.Surface((250,75))
    playRect.set_alpha(196)
    rulesRect.set_alpha(196)
    playRect.fill(green)
    rulesRect.fill(blue)
    screen.blit(playRect,(50,500))
    screen.blit(rulesRect,(WIDTH-300,500))
    screen.blit(play,(130,515))
    screen.blit(rules,(WIDTH-235,515))
    pygame.display.update()
    
def end_screen():
    screen.blit(endScreen,(0,0))                            # This function draws the end screen
    scores = myFont.render("Score: "+str(score),1,WHITE)    # and the final score of the game
    screen.blit(scores,(315,25))            
    pygame.display.update()                 
    
def rulesScreen():
    screen.blit(introScreen,(0,0))          # This function draws the intro screen with
    rulesList = pygame.Surface((500,300))   # The Rules are drawn onto the screen for the player to read
    rulesList.set_alpha(196)                # There is also a play button that if clicked will start the game
    rulesList.fill(red)
    screen.blit(rulesList,(150,225))
    playRect = pygame.Surface((250,75))
    playRect.set_alpha(196)
    playRect.fill(green)
    screen.blit(playRect,(275,525))
    screen.blit(play,(355,540))
    rules1 = myFont.render("RULES:",1,BLACK)
    rules2 = myFont2.render("1. Press space to instantly move down",1,BLACK)
    rules3 = myFont2.render("2. 1 Full row is 100 Points, a Tetris is 800 Points",1,BLACK)
    rules4 = myFont2.render("Back to Back Tetris' is 1200 Points:",1,BLACK)
    rules5 = myFont2.render("3. 500 Points to Clear level 1 and 1000 to clear level 2",1,BLACK)
    rules6 = myFont2.render("4. Press Left Shift to put/take a shape into/out of hold ",1,BLACK)
    rules7 = myFont3.render("5. When you fill 1 column to the top, the game is over and you lose",1,BLACK)
    screen.blit(rules1,(325,225))
    screen.blit(rules2,(150,267))
    screen.blit(rules3,(150,309))
    screen.blit(rules4,(175,351))
    screen.blit(rules5,(150,393))
    screen.blit(rules6,(150,435))
    screen.blit(rules7,(150,477))
    pygame.display.update()
                
                        
#---------------------------------------#
#   main program                        #
#---------------------------------------#


if introS:                                                              # Plays the music if the boolean is true
    tetrisIntro.play(-1)
while introS:                                                           # While the boolean is true, the intro screen is run
    intro_screen()                                                      # Checks if the play button is clicked, if it is, runs the game
    for event in pygame.event.get():                                    # Checks if the rules button is clicked, if it is, runs the rules function
        if event.type == pygame.QUIT:         
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            (cursorX,cursorY)=pygame.mouse.get_pos()
            if 50+250 > cursorX > 50 and 500+75 > cursorY > 500:
                introS = False
                inPlay = True
                tetrisIntro.stop()
                perftime = time.perf_counter()
            if WIDTH-300 < cursorX < WIDTH-50 and 500+75 > cursorY > 500:
                introS = False
                rulesS = True
while rulesS:                                                           # While the boolean is true, the rules screen is run
    rulesScreen()                                                       # Checks if the play button is clicked, if it is, runs the game
    for event in pygame.event.get():                                    
        if event.type == pygame.QUIT:         
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            (cursorX,cursorY)=pygame.mouse.get_pos()
            if 275+250 > cursorX > 275 and 525+75 > cursorY > 525:
                rulesS = False
                inPlay = True
                tetrisIntro.stop()
                perftime = time.perf_counter()
if inPlay:                                                              # Plays the music if the boolean is true
    music.play(-1)
while inPlay:
    shadow.moveShadow(floor,obstacle,shape)                             # While the boolean is true, the game is run
    shape.move_down()
    if shape.collides(floor) or shape.collides(obstacle):               # Checks for collision and then runs through commands that
        shape.move_up()                                                 # Will play the sound, make the shape an obstacle, redraw
        land.play()                                                     # the shapes and the shadow when the first shape becomes an obstacle
        obstacle.append(shape)
        fullRows = obstacle.findFullRows(TOP, FLOOR, COLUMNS)           # finds the full rows and removes their blocks from the obstacles 
        obstacle.removeFullRows(fullRows)
        score = scoring.scoreSystem(fullRows,lineClear,tetrisClear)
        shapeNo = shapeNo2
        shapeNo2 = randint(1,7)
        shape = Shape(MIDDLE,TOP+2,shapeNo)
        nextShape = Shape(MIDDLE+11,TOP+10,shapeNo2)
        shadow = Shape(MIDDLE,TOP+2,shapeNo)
        
    for event in pygame.event.get():                                    
        if event.type == pygame.QUIT:                                        # Quits the game   
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:                                     # If the key button is up, rotates the shape and shadow clockwise
                shape.rotateClkwise()
                shadow.rotateClkwise()
                if shape.collides(leftWall) or shape.collides(rightWall) or shape.collides(floor) or shape.collides(obstacle):          # If the shape/shadow collides with a wall or shape, rotates it counter clockwise
                    shape.rotateCntclkwise()
                    shadow.rotateCntclkwise()
            if event.key == pygame.K_LEFT:                                   # If the key button is left, moves the shape and shadow to the left
                shape.move_left()
                shadow.move_left()
                if shape.collides(leftWall) or shape.collides(obstacle):     # If the shape/shadow collides with a wall, moves the shape and shadow to the right
                    shape.move_right()
                    shadow.move_right()
            if event.key == pygame.K_RIGHT:                                  # If the key button is right, moves the shape and shadow to the right
                shape.move_right()
                shadow.move_right()
                if shape.collides(rightWall) or shape.collides(obstacle):    # If the shape/shadow collides with a wall, moves the shape and shadow to the right
                    shape.move_left()
                    shadow.move_left()
            if event.key == pygame.K_DOWN:                                   # If the key button is down, moves the shape downwards
                shape.move_down()
                if shape.collides(floor) or shape.collides(obstacle):        # If the shape collides with the floor or an obstacle, moves the shape up and runs the same collision commands as before
                    shape.move_up()
                    land.play()
                    obstacle.append(shape)
                    fullRows = obstacle.findFullRows(TOP, FLOOR, COLUMNS)    # finds the full rows and removes their blocks from the obstacles 
                    obstacle.removeFullRows(fullRows)
                    score = scoring.scoreSystem(fullRows,lineClear,tetrisClear)
                    shapeNo = shapeNo2
                    shapeNo2 = randint(1,7)
                    shape = Shape(MIDDLE,TOP+2,shapeNo)
                    nextShape = Shape(MIDDLE+11,TOP+10,shapeNo2)
                    shadow = Shape(MIDDLE,TOP+2,shapeNo)
            if event.key == pygame.K_SPACE:                                  # If the space key is pressed, instantly drops the shape to the bottom
                while not shape.collides(floor) and not shape.collides(obstacle):   
                    shape.move_down()
                if shape.collides(floor) or shape.collides(obstacle):        # If the shape collides with the floor or an obstacle, moves the shape up and runs the same collision commands as before
                    shape.move_up()
                    land.play()
                    obstacle.append(shape)
                    fullRows = obstacle.findFullRows(TOP, FLOOR, COLUMNS)    # finds the full rows and removes their blocks from the obstacles 
                    obstacle.removeFullRows(fullRows)
                    score = scoring.scoreSystem(fullRows,lineClear,tetrisClear)
                    shapeNo = shapeNo2
                    shapeNo2 = randint(1,7)
                    shape = Shape(MIDDLE,TOP+2,shapeNo)
                    nextShape = Shape(MIDDLE+11,TOP+10,shapeNo2)
                    shadow = Shape(MIDDLE,TOP+2,shapeNo)
            if event.key == pygame.K_LSHIFT:                                 # If the Left Shift key is pressed, it will put the block on hold
                if currentHold:                                              # If the block is currently on hold and the Left Shift key is pressed,
                    shapeNo = holdShapeNo                                    # the block will be removed from hold and will be instantly used instead of the shape
                    holdShapeNo = 0                                          # If there is no shape in hold and the Left Shift key is pressed,
                    if holdShapeNo != 0:                                     # the block will be moved into hold and the next shape will replace the current shaoe
                        holdShape = Shape(MIDDLE+20,TOP+10,holdShapeNo)
                    shape = Shape(MIDDLE,TOP+2,shapeNo)
                    shadow = Shape(MIDDLE,TOP+2,shapeNo)
                    currentHold = False
                    continue
                if currentHold == False:
                    holdShapeNo = shapeNo
                    shapeNo = shapeNo2
                    if holdShapeNo != 5:
                        holdShape = Shape(MIDDLE+20,TOP+10,holdShapeNo)
                    else:
                        holdShape = Shape(MIDDLE+19,TOP+10,holdShapeNo)
                    shapeNo2 = randint(1,7)
                    shape = Shape(MIDDLE,TOP+2,shapeNo)
                    nextShape = Shape(MIDDLE+11,TOP+10,shapeNo2)
                    shadow = Shape(MIDDLE,TOP+2,shapeNo)
                    currentHold = True
    if obstacle.collides(roof):                                              # If the obstacle hits the roof, the game will end and a sound will play
        music.stop()
        tetrisGameOver.play()
        endS = True
        inPlay = False
        
    shadow.moveShadow(floor,obstacle,shape)
    timer = (time.perf_counter()-perftime)
    level, delay = scoring.changeSpeed()
    redraw_screen()
    pygame.time.delay(delay)

while endS:                                                                  # If the game is over, the end screen function will be run
    end_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:         
            pygame.quit()
            sys.exit()
    
    
pygame.quit()
sys.exit()
    
    
