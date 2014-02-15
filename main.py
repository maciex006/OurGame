import sys
import pygame
from pygame.locals import *

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

WINDOW_RESOLUTION = (400, 300)
WINDOW_CENTER = [int(WINDOW_RESOLUTION[0]/2), int(WINDOW_RESOLUTION[1]/2)]
HERO_POSITION = [int(WINDOW_RESOLUTION[0]/2), int(WINDOW_RESOLUTION[1]/2)]
WINDOW_NAME = "OurGame"
FPS = 30

BACKGROUND_SOURCE = 'images/background.png'
BACKGROUND_IMG = pygame.image.load(BACKGROUND_SOURCE)
BACKGROUND_POSX = -100
BACKGROUND_POSY = -100
MAP_WID = 1024
MAP_HEI = 768
STEP = 10

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
	global BACKGROUND_POSX, BACKGROUND_POSY, WINDOW_RESOLUTION, STEP, MAP_HEI, MAP_WID
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



def heroCollisionCheck():
	pass


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
        
        #our weird background
        setDisplay.blit(BACKGROUND_IMG,(BACKGROUND_POSX, BACKGROUND_POSY))
        
        #hero
        pygame.draw.circle(setDisplay, RED, WINDOW_CENTER, 10)
        
        pygame.display.update()
        FPS_TIME.tick(FPS)

#loadGame()

while True:
    global FPS_TIME
    FPS_TIME = pygame.time.Clock()
    runGame()
    