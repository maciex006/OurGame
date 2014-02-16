import sys
import pygame
import numpy
from pygame.locals import *

from create_box import create_box

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

a = (210,268)
b = (385,216)
c = (406,473)
d = (596,394)
    
DIM_X =  1024
DIM_Y =  728

POINTS = ( a , b , c , d )

MATRIX = create_box ( DIM_X , DIM_Y , POINTS )

#####################

BACKGROUND_SOURCE = 'images/background.png'
BACKGROUND_IMG = pygame.image.load(BACKGROUND_SOURCE)
BACKGROUND_POSX = -100
BACKGROUND_POSY = -100
MAP_WID = 1024
MAP_HEI = 768
STEP = 1

WINDOW_RESOLUTION = (400, 300)
WINDOW_CENTER = [int(WINDOW_RESOLUTION[0]/2), int(WINDOW_RESOLUTION[1]/2)]
HERO_POSITION = [BACKGROUND_POSX + int(WINDOW_RESOLUTION[0]/2), BACKGROUND_POSY + int(WINDOW_RESOLUTION[1]/2)]
WINDOW_NAME = "OurGame"
FPS = 60

HERO_SPEED = 1

setDisplay = pygame.display.set_mode(WINDOW_RESOLUTION)
pygame.display.set_caption(WINDOW_NAME)

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
    return MATRIX[x,y]

def animateHeroMovement(x0, y0, x, y):
    global BACKGROUND_POSX
    global BACKGROUND_POSY
    global HERO_SPEED
    #BACKGROUND_POSX = x
    #BACKGROUND_POSY = y

    d = numpy.sqrt((x-x0)*(x-x0)+(y-y0)*(y-y0))
    if ((x-x0) != 0):
        a = numpy.arctan(numpy.fabs(y-y0)/numpy.fabs(x-x0))
    else:
        a = 0

    print(d)
    print(a)

    print(x0)
    print(y0)
    print(x)
    print(y)

    new_d = STEP

    bgx = BACKGROUND_POSX
    bgy = BACKGROUND_POSY

    while ( new_d < d ):
        print(new_d)
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

        print("1: " + str(newx) + " , " + str(newy))

        BACKGROUND_POSX = newx
        BACKGROUND_POSY = newy
        pygame.time.wait(HERO_SPEED)
        new_d += STEP
        drawGame()


    new_d = d
    BACKGROUND_POSX = x
    BACKGROUND_POSY = y
    print(x)
    print(y)

    # for a -> b:
    #     step x
    #     step y
    #     drawGame()

def moveHero(x, y):
    global BACKGROUND_POSX
    global BACKGROUND_POSY
    global HERO_POSITION
    currentX = BACKGROUND_POSX
    currentY = BACKGROUND_POSY

    x2 = x - BACKGROUND_POSX
    y2 = y - BACKGROUND_POSY

    if heroCollisionCheck(x2, y2):
        targetX = BACKGROUND_POSX - x + WINDOW_RESOLUTION[0]/2
        targetY = BACKGROUND_POSY - y + WINDOW_RESOLUTION[1]/2
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
    while True:
        #events
        for event in pygame.event.get():
            #print event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos() # (x, y)
                print mousePosition
                moveHero(mousePosition[0], mousePosition[1])

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
    