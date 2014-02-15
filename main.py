import sys
import pygame
from pygame.locals import *

pygame.init()

#CONSTS
WINDOW_RESOLUTION = (400, 300)
WINDOW_NAME = ""

BACKGROUND_SOURCE = 'images/background.png'
BACKGROUND_IMG = pygame.image.load(BACKGROUND_SOURCE)

#ustawiamy okno
setDisplay = pygame.display.set_mode(WINDOW_RESOLUTION)
pygame.display.set_caption(WINDOW_NAME)

while True:
	pass