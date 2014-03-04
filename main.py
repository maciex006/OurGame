import sys
import pygame
import time
import numpy

from pygame.locals import *

from create_box import create_box
from create_box import load_box
from path_finder import find_path

pygame.init()

########
#CONSTS#
########
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

# matrix generation #
#####################
    
DIM_X =  1024
DIM_Y =  728

MATRIX = []

#a = (579,407)
#b = (595,480)
outa = (566,398),(586,418)
ina = (586,418),(566,398)
outb = (586,486),(611,468)
inb = (611,468),(586,486)
line1 = (1, (outa,2))
line2 = (2, (ina,1),(inb,3))
line3 = (3, (outb,2))
DATA = ( line1, line2, line3 )

#####################

BACKGROUND_SOURCE = 'images/background.png'
BACKGROUND_IMG = pygame.image.load(BACKGROUND_SOURCE)
BACKGROUND_POSX = -100
BACKGROUND_POSY = -120
MAP_WID = 1024
MAP_HEI = 768
STEP = 1

WINDOW_RESOLUTION = (550, 450)
WINDOW_CENTER = [int(WINDOW_RESOLUTION[0]/2), int(WINDOW_RESOLUTION[1]/2)]
HERO_POSITION = [BACKGROUND_POSX + int(WINDOW_RESOLUTION[0]/2), BACKGROUND_POSY + int(WINDOW_RESOLUTION[1]/2)]
WINDOW_NAME = "OurGame"
FPS = 60

HERO_SPEED = 25
HERO_WALK = 1
HERO_RUN = 2

setDisplay = pygame.display.set_mode(WINDOW_RESOLUTION)
pygame.display.set_caption(WINDOW_NAME)

def detectDoubleClick():
    initTime = time.clock()
    while time.clock() - initTime < 0.15:
        for event in pygame.event.get([MOUSEBUTTONDOWN]):
            if event.type == MOUSEBUTTONDOWN:
                return True
    return False

def loadGame():
    global MATRIX
    notReady = True
    setDisplay.fill(BLACK)
    pygame.draw.rect(setDisplay, RED, (int(WINDOW_RESOLUTION[0]/8), int(WINDOW_RESOLUTION[1]/4)*3, int(WINDOW_RESOLUTION[0]/8)*6, int(WINDOW_RESOLUTION[1]/8)), 2)
    pygame.display.update()
    #pygame.time.wait(500)
    MATRIX = load_box( DIM_X , DIM_Y , "map_input.txt" )

    for i in range(1, 7):
        pygame.draw.rect(setDisplay, WHITE, (int(WINDOW_RESOLUTION[0]/8), int(WINDOW_RESOLUTION[1]/4)*3, int(WINDOW_RESOLUTION[0]/8)*i, int(WINDOW_RESOLUTION[1]/8)))
        pygame.draw.rect(setDisplay, RED, (int(WINDOW_RESOLUTION[0]/8), int(WINDOW_RESOLUTION[1]/4)*3, int(WINDOW_RESOLUTION[0]/8)*6, int(WINDOW_RESOLUTION[1]/8)), 2)
        pygame.display.update()
        pygame.time.wait(100)

def screenBoundsCheck(minus = False, axisX = False, axisY = False):
    global BACKGROUND_POSX, BACKGROUND_POSY
    if minus:
        if (BACKGROUND_POSX - STEP + MAP_WID >= WINDOW_RESOLUTION[0]) and axisX:
            BACKGROUND_POSX -= STEP
        if (BACKGROUND_POSY - STEP + MAP_HEI >= WINDOW_RESOLUTION[1]) and axisY:
            BACKGROUND_POSY -= STEP
    else:
        if (BACKGROUND_POSX + STEP <= 0) and axisX:
            BACKGROUND_POSX += STEP
        if (BACKGROUND_POSY + STEP <= 0) and axisY:
            BACKGROUND_POSY += STEP

def heroCollisionCheck(x, y):
    return MATRIX[x,y]

def animateHeroMovement(x0, y0, x, y):
    global BACKGROUND_POSX
    global BACKGROUND_POSY
    global HERO_SPEED

    d = numpy.sqrt((x-x0)*(x-x0)+(y-y0)*(y-y0))
    if ((x-x0) != 0):
        a = numpy.arctan(numpy.fabs(y-y0)/numpy.fabs(x-x0))
    else:
        a = 0

    new_d = STEP
    
    mouseNotClicked = True

    while ( new_d < d ) and (mouseNotClicked):
        if ( x > x0 ):
            if ( y < y0 ):
                newx = x - (d - new_d)*numpy.cos(a)
                newy = y + (d - new_d)*numpy.sin(a)
            else:
                newx = x - (d - new_d)*numpy.cos(a)
                newy = y - (d - new_d)*numpy.sin(a)
        else:
            if ( y < y0 ):
                newx = x + (d - new_d)*numpy.cos(a)
                newy = y + (d - new_d)*numpy.sin(a)
            else:
                newx = x + (d - new_d)*numpy.cos(a)
                newy = y - (d - new_d)*numpy.sin(a)


        if heroCollisionCheck(newx, newy):
            BACKGROUND_POSX = WINDOW_RESOLUTION[0]/2 - newx
            BACKGROUND_POSY = WINDOW_RESOLUTION[1]/2 - newy
            pygame.time.wait(HERO_SPEED)
            new_d += STEP
            drawGame()
        else:
            return -1


        #click check
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                #checking for double click
                mouseNotClicked = False
                mousePosition = pygame.mouse.get_pos()
                
                if detectDoubleClick():
                    HERO_SPEED = HERO_RUN
                else:
                    HERO_SPEED = HERO_WALK
                
                return moveHero(translate(mousePosition[0], mousePosition[1]))
                    

    if mouseNotClicked:
        new_d = d
        BACKGROUND_POSX = WINDOW_RESOLUTION[0]/2 - x
        BACKGROUND_POSY = WINDOW_RESOLUTION[1]/2 - y


def translate(x , y):
    global BACKGROUND_POSX
    global BACKGROUND_POSY
    return (int(x - BACKGROUND_POSX),int(y - BACKGROUND_POSY))

def moveHero( position ):
    print("Nowy klik!")
    targetX = position[0]
    targetY = position[1]

    global BACKGROUND_POSX
    global BACKGROUND_POSY

    #currentX = BACKGROUND_POSX
    #currentY = BACKGROUND_POSY

    currentX = - BACKGROUND_POSX + WINDOW_RESOLUTION[0]/2
    currentY = - BACKGROUND_POSY + WINDOW_RESOLUTION[1]/2

    targetChamber = heroCollisionCheck(targetX, targetY)
    currentChamber = heroCollisionCheck(currentX, currentY)

    if targetChamber != 0:
        if ( targetChamber == currentChamber ):
            print( "pozycja1:" + str(currentX) + "," +str(currentY))
            print( "cel1:" + str(targetX) + "," +str(targetY))

            animateHeroMovement(currentX, currentY, targetX, targetY)
        else:

            path = find_path(int(currentChamber),int(targetChamber),DATA)
            print(path)
            for i in range(len(path[0])):
                for j in range (2):
                    targetX = int(path[0][i][j][0])
                    targetY = int(path[0][i][j][1])

                    print( "pozycja2:" + str(currentX) + "," +str(currentY))
                    print( "cel2:" + str(targetX) + "," +str(targetY))

                    animateHeroMovement(currentX, currentY, targetX , targetY)
                    currentX = - BACKGROUND_POSX + WINDOW_RESOLUTION[0]/2
                    currentY = - BACKGROUND_POSY + WINDOW_RESOLUTION[1]/2


            targetX = position[0]
            targetY = position[1]
            print( "pozycja3:" + str(currentX) + "," +str(currentY))
            print( "cel3:" + str(targetX) + "," +str(targetY))
            animateHeroMovement(currentX, currentY , targetX , targetY)

from engineClass import dynamicObject
npc2 = dynamicObject('Stworek2', (655,415)) # 655,415
#GAME_OBJECTS = {npc1.getPosition():npc1}
GAME_OBJECTS = [npc2]

npc1 = dynamicObject('Potworek2', (655,415))
npc2 = dynamicObject('Stworek2', (360, 400))
npc3 = dynamicObject('Horrorek3', (484, 541))
hero = dynamicObject('Hero', (WINDOW_CENTER[0]-BACKGROUND_POSX, WINDOW_CENTER[1]-BACKGROUND_POSY))

#GAME_OBJECTS = {npc1.getPosition():npc1}
GAME_OBJECTS = [npc1, npc2, npc3]
print GAME_OBJECTS
for e in GAME_OBJECTS:
    e.setTarget(390, 340)

def sigKill():
    pygame.quit()
    sys.exit()

def drawGame():
        global BACKGROUND_POSX
        global BACKGROUND_POSY

        #our weird background
        setDisplay.blit(BACKGROUND_IMG,(BACKGROUND_POSX, BACKGROUND_POSY))
        #gameObjects and our hero
        for npc in GAME_OBJECTS:
            #npc.move(MATRIX,DATA)
            npcPos = npc.getPosition()
            npcX = int(npcPos[0] + BACKGROUND_POSX)
            npcY = int(npcPos[1] + BACKGROUND_POSY)
            pygame.draw.circle(setDisplay, GREEN, (npcX, npcY), 5)

        hero.move(MATRIX, DATA)
        heroPos = hero.getPosition()
        heroX = int(heroPos[0] + BACKGROUND_POSX)
        heroY = int(heroPos[1] + BACKGROUND_POSY)
        BACKGROUND_POSX = - heroPos[0] + WINDOW_CENTER[0]
        BACKGROUND_POSY = - heroPos[1] + WINDOW_CENTER[1]
        pygame.draw.circle(setDisplay, RED, (heroX, heroY), 10)

        pygame.display.update()
        FPS_TIME.tick(FPS)

def runGame():
    global BACKGROUND_POSX
    global BACKGROUND_POSY
    global HERO_SPEED
    while True:
        #events
        for event in pygame.event.get():
            #print event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                #checking for double click
                if detectDoubleClick():
                    #HERO_SPEED = HERO_RUN
                    hero.setStep(HERO_RUN)
                else:
                    #HERO_SPEED = HERO_WALK
                    hero.setStep(HERO_WALK)


                mousePosition = pygame.mouse.get_pos() # (x, y)
                #print mousePosition

                hero.setTarget(translate(mousePosition[0], mousePosition[1])[0],translate(mousePosition[0], mousePosition[1])[1])


        keys = pygame.key.get_pressed()
        if keys[K_UP] or keys[K_w]:
            #BACKGROUND_POSY += STEP
            screenBoundsCheck(False, False, True)
            HERO_POSITION[1] += STEP
        elif keys[K_DOWN] or keys[K_s]:
            #BACKGROUND_POSY -= STEP
            screenBoundsCheck(True, False, True)
            HERO_POSITION[1] -= STEP
        if keys[K_LEFT] or keys[K_a]:
            #BACKGROUND_POSX += STEP
            screenBoundsCheck(False, True, False)
            HERO_POSITION[0] += STEP
        elif keys[K_RIGHT] or keys[K_d]:
            #BACKGROUND_POSX -= STEP
            screenBoundsCheck(True, True, False)
            HERO_POSITION[0] -= STEP
        
        drawGame()
        
#loadGame()

while True:
    global FPS_TIME
    FPS_TIME = pygame.time.Clock()
    loadGame()
    runGame()
    