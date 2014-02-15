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
HERO_POSITION = (int(WINDOW_RESOLUTION[0]/2), int(WINDOW_RESOLUTION[1]/2))
WINDOW_NAME = ""
FPS = 60

BACKGROUND_SOURCE = 'images/background.png'
BACKGROUND_IMG = pygame.image.load(BACKGROUND_SOURCE)
BACKGROUND_POSX = 0
BACKGROUND_POSY = 0
STEP = 10

#ustawiamy okno
setDisplay = pygame.display.set_mode(WINDOW_RESOLUTION)
pygame.display.set_caption(WINDOW_NAME)

def runGame():
    global BACKGROUND_POSX
    global BACKGROUND_POSY
    while True:
        #eventy
        for event in pygame.event.get():
            print event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            #BACKGROUND_POSX = STEP
            BACKGROUND_POSY -= STEP
        elif keys[K_DOWN]:
            #BACKGROUND_POSX = STEP
            BACKGROUND_POSY += STEP
        if keys[K_LEFT]:
            BACKGROUND_POSX -= STEP
            #BACKGROUND_POSY = STEP
        elif keys[K_RIGHT]:
            BACKGROUND_POSX += STEP
            #BACKGROUND_POSY = STEP
                    
        
        #wyswietlnie obrazka
        setDisplay.blit(BACKGROUND_IMG,(BACKGROUND_POSX, BACKGROUND_POSY))
        
        #gostek
        pygame.draw.circle(setDisplay, RED, HERO_POSITION, 55)
        
        pygame.display.update()
        FPS_TIME.tick(FPS)

while True:
    global FPS_TIME
    FPS_TIME = pygame.time.Clock()
    runGame()
