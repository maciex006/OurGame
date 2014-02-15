__author__ = 'maciex'

import numpy

a = (210,268)
b = (385,216)
d = (406,473)
c = (596,394)

DIM_X =  700
DIM_Y =  700

POINTS = ( a , b , c , d )

def create_box ( DIM_X , DIM_Y , POINTS ):
    matrix = numpy.zeros(shape=(DIM_X,DIM_Y))


    def solve( (x1 , y1) , (x2 , y2) ):
        ARRAY_1 = numpy.array([[x1,1], [x2,1]])
        ARRAY_2 = numpy.array([y1,y2])
        return numpy.linalg.solve(ARRAY_1, ARRAY_2)

    line1 = solve( POINTS[0] , POINTS[1] )
    print (line1)
    line2 = solve( POINTS[0] , POINTS[2] )
    print (line2)
    line3 = solve( POINTS[2] , POINTS[3] )
    print (line3)
    line4 = solve( POINTS[1] , POINTS[3] )
    print (line4)


    for i in range(POINTS[0][0],POINTS[1][0]):
        for j in range(0,DIM_Y):
            if ( ( j < ( line1[0]*i + line1[1] )) and ( j > ( line2[0]*i + line2[1] )) ):
                matrix[i,j] = 1

    for i in range(POINTS[1][0],POINTS[2][0]):
        for j in range(0,DIM_Y):
            if ( ( j < ( line4[0]*i + line4[1] )) and ( j > ( line2[0]*i + line2[1] )) ):
                matrix[i,j] = 1

    for i in range(POINTS[2][0],POINTS[3][0]):
        for j in range(0,DIM_Y):
            if ( ( j < ( line4[0]*i + line4[1] )) and ( j > ( line3[0]*i + line3[1] )) ):
                matrix[i,j] = 1

    return matrix
  


import pickle 

matrix = create_box(DIM_X, DIM_Y, POINTS)

# try:
#     f = open("file.txt", "w")
#     pickle.dump(matrix, f)
# finally:
#     f.close()

# b =[]

# try:
#     fi = open("file.txt", "r")
#     b = pickle.load(fi)
# finally:
#     fi.close()

import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

setDisplay = pygame.display.set_mode((DIM_X,DIM_Y))
setDisplay.fill(WHITE)

pixele = pygame.PixelArray(setDisplay)
for n in range(0, DIM_X):
    for m in range(0, DIM_Y):
        if matrix[n][m] == 0:
            pixele[n][m] = BLACK
        else:
            pixele[n][m] = WHITE
    pygame.display.update()

pygame.display.update()

raw_input()