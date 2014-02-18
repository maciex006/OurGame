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

MATRIX = load_box( DIM_X , DIM_Y , "map_input.txt" )

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
BACKGROUND_POSY = -100
MAP_WID = 1024
MAP_HEI = 768
STEP = 1

WINDOW_RESOLUTION = (550, 450)
WINDOW_CENTER = [int(WINDOW_RESOLUTION[0]/2), int(WINDOW_RESOLUTION[1]/2)]
HERO_POSITION = [BACKGROUND_POSX + int(WINDOW_RESOLUTION[0]/2), BACKGROUND_POSY + int(WINDOW_RESOLUTION[1]/2)]
WINDOW_NAME = "OurGame"
FPS = 60

HERO_SPEED = 25
HERO_WALK = 25
HERO_RUN = 10

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
    notReady = True
    setDisplay.fill(BLACK)
    pygame.draw.rect(setDisplay, RED, (int(WINDOW_RESOLUTION[0]/8), int(WINDOW_RESOLUTION[1]/4)*3, int(WINDOW_RESOLUTION[0]/8)*6, int(WINDOW_RESOLUTION[1]/8)), 2)
    pygame.display.update()
    pygame.time.wait(500)

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
    #print(str(x) + "," + str(y))
    #print(MATRIX[x,y])
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

        #if heroCollisionCheck(-newx + WINDOW_RESOLUTION[0]/2, -newy + WINDOW_RESOLUTION[1]/2):
        #    BACKGROUND_POSX = newx
        #    BACKGROUND_POSY = newy
        #    pygame.time.wait(HERO_SPEED)
        #    new_d += STEP
        #    drawGame()
        #else:
        #    return -1

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

    currentChamber = heroCollisionCheck(targetX, targetY)
    targetChamber = heroCollisionCheck(currentX, currentY)
    
    if targetChamber != 0:
        if ( targetChamber == currentChamber ):
            print( "pozycja1:" + str(currentX) + "," +str(currentY))
            print( "cel1:" + str(targetX) + "," +str(targetY))

            animateHeroMovement(currentX, currentY, targetX, targetY)
        else:

            path = find_path(int(targetChamber),int(currentChamber),DATA)
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
            animateHeroMovement(currentX, currentY,targetX, targetY)


def drawGame():
        #our weird background
        setDisplay.blit(BACKGROUND_IMG,(BACKGROUND_POSX, BACKGROUND_POSY))
        #hero
        pygame.draw.circle(setDisplay, RED, WINDOW_CENTER, 10)
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
                    HERO_SPEED = HERO_RUN
                else:
                    HERO_SPEED = HERO_WALK


                mousePosition = pygame.mouse.get_pos() # (x, y)
                #print mousePosition

                moveHero(translate(mousePosition[0], mousePosition[1]))

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
    runGame()
    