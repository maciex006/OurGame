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

###########################################

TABLE_SOURCE = 'images/edit_table1.png'
TABLE_IMG = pygame.image.load(TABLE_SOURCE)
TABLE_POSX = 270
TABLE_POSY = 220

###########################################

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

def translate(x , y):
    global BACKGROUND_POSX
    global BACKGROUND_POSY
    return (int(x - BACKGROUND_POSX),int(y - BACKGROUND_POSY))


from engineClass import dynamicObject
from engineClass import staticObject
npc2 = dynamicObject('Stworek2', (655,415)) # 655,415
#GAME_OBJECTS = {npc1.getPosition():npc1}
GAME_OBJECTS = [npc2]

npc1 = dynamicObject('Potworek2', (655,415))
npc2 = dynamicObject('Stworek2', (360, 400))
npc3 = dynamicObject('Horrorek3', (484, 541))
hero = dynamicObject('Hero', (WINDOW_CENTER[0]-BACKGROUND_POSX, WINDOW_CENTER[1]-BACKGROUND_POSY))
STATIC_OBJECTS = [0]
STATIC_OBJECTS = STATIC_OBJECTS + [ staticObject('Stol', (TABLE_POSX, TABLE_POSY) , -1, TABLE_IMG) ]

STANDING_POINTS = [0]
STANDING_POINTS = STANDING_POINTS + [ (316,325) ]

#GAME_OBJECTS = {npc1.getPosition():npc1}
GAME_OBJECTS = [npc1, npc2, npc3]
for e in GAME_OBJECTS:
    e.setTarget(390, 340)

def sigKill():
    pygame.quit()
    sys.exit()

here = 0

def drawGame():
        global BACKGROUND_POSX
        global BACKGROUND_POSY

        #hero moving
        correction = -1
        if (hero.move(MATRIX, DATA)):
            correction = 0
        heroPos = hero.getPosition()
        heroX = int(heroPos[0] + BACKGROUND_POSX)
        heroY = int(heroPos[1] + BACKGROUND_POSY)
        BACKGROUND_POSX = - heroPos[0] + WINDOW_CENTER[0]
        BACKGROUND_POSY = - heroPos[1] + WINDOW_CENTER[1]

        #our weird background a
        setDisplay.blit(BACKGROUND_IMG,(BACKGROUND_POSX, BACKGROUND_POSY))



        mousePosition = pygame.mouse.get_pos()
        matrixPosition = MATRIX[ mousePosition[0] - BACKGROUND_POSX][mousePosition[1] - BACKGROUND_POSY ]
        for i in range(1,len(STATIC_OBJECTS)):
            if ( matrixPosition == -i ):
                setDisplay.blit(STATIC_OBJECTS[i].getGraphic(), (BACKGROUND_POSX+STATIC_OBJECTS[i].getPosition()[0]+correction, BACKGROUND_POSY+STATIC_OBJECTS[i].getPosition()[1]+correction))
            if ( heroPos == STANDING_POINTS[i] and here == 0):
                print("DOSZEDL!")
                global here
                here = 1
                #TUUUUUUTAJ WYSWIETLENIE OKIENKA

        pygame.draw.circle(setDisplay, RED, (heroX, heroY), 10)

        #gameObjects
        for npc in GAME_OBJECTS:
            npc.move(MATRIX,DATA)
            npcPos = npc.getPosition()
            npcX = int(npcPos[0] + BACKGROUND_POSX + correction)
            npcY = int(npcPos[1] + BACKGROUND_POSY + correction)
            pygame.draw.circle(setDisplay, GREEN, (npcX, npcY), 5)


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
                hero.setTarget(translate(mousePosition[0], mousePosition[1])[0],translate(mousePosition[0], mousePosition[1])[1])
                global here
                here = 0
                matrixPosition = MATRIX[ mousePosition[0] - BACKGROUND_POSX][mousePosition[1] - BACKGROUND_POSY ]
                for i in range(1,len(STATIC_OBJECTS)): # przeszukiwanie tablicy obiektow statycznych
                    if ( matrixPosition == -i ):
                        hero.setTarget(STANDING_POINTS[i][0],STANDING_POINTS[i][1])




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
    