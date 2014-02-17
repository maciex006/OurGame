__author__ = 'maciex'

import numpy

DIM_X =  1024
DIM_Y =  728

def create_box ( DIM_X , DIM_Y , POINTS , matrix ):

    def solve( (x1 , y1) , (x2 , y2) ):
        ARRAY_1 = numpy.array([[x1,1], [x2,1]])
        ARRAY_2 = numpy.array([y1,y2])
        return numpy.linalg.solve(ARRAY_1, ARRAY_2)

    if ( POINTS[0][1]  < POINTS[1][1]):
        line1 = solve( POINTS[0] , POINTS[1] )
        line2 = solve( POINTS[0] , POINTS[2] )
        line3 = solve( POINTS[2] , POINTS[3] )
        line4 = solve( POINTS[1] , POINTS[3] )

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

    else:
        line2 = solve( POINTS[0] , POINTS[1] )
        line1 = solve( POINTS[0] , POINTS[2] )
        line4 = solve( POINTS[2] , POINTS[3] )
        line3 = solve( POINTS[1] , POINTS[3] )

        for i in range(POINTS[0][0],POINTS[1][0]):
            for j in range(0,DIM_Y):
                if ( ( j < ( line1[0]*i + line1[1] )) and ( j > ( line2[0]*i + line2[1] )) ):
                    matrix[i,j] = 1

        for i in range(POINTS[1][0],POINTS[2][0]):
            for j in range(0,DIM_Y):
                if ( ( j < ( line1[0]*i + line1[1] )) and ( j > ( line3[0]*i + line3[1] )) ):
                    matrix[i,j] = 1

        for i in range(POINTS[2][0],POINTS[3][0]):
            for j in range(0,DIM_Y):
                if ( ( j < ( line4[0]*i + line4[1] )) and ( j > ( line3[0]*i + line3[1] )) ):
                    matrix[i,j] = 1

    return matrix


def load_box( DIM_X , DIM_Y , map_input_path ):
    with open(map_input_path, 'r') as map_input:
        map_input = map_input.readlines()
        map_input = [ e.strip() for e in map_input ]
        map_output = []
        #wywalanie komentarzy
        for e in map_input:
            if '#' not in e:
                comma = e.index(",")
                map_output.append(int(e[:comma]))
                map_output.append(int(e[comma+1:]))
        map_len = len(map_output)
        #sprawdzamy czy mamy krotnosc 8 linii poza komentarzami
        if map_len % 8 != 0:
            print "map input format error"
            raise ValueError
        
        matrix = numpy.zeros(shape=(DIM_X,DIM_Y))
        for i in range(0,len(map_output),8):
            print i
            a = (map_output[i], map_output[i+1])
            b = (map_output[i+2], map_output[i+3])
            c = (map_output[i+4], map_output[i+5])
            d = (map_output[i+6], map_output[i+7])
            points = (a, b, c, d)
            matrix = create_box(DIM_X, DIM_Y, points, matrix)
            
        return matrix


#python createbox
if __name__ == "__main__":

    import pygame

    matrix = load_box( DIM_X , DIM_Y , "map_input.txt" )

    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    setDisplay = pygame.display.set_mode((DIM_X, DIM_Y))
    setDisplay.fill(WHITE)

    pixele = pygame.PixelArray(setDisplay)
    for n in range(0, DIM_X):
        for m in range(0, DIM_Y):
            if matrix[n][m] == 0:
                pixele[n][m] = BLACK
            else:
                pixele[n][m] = WHITE

    pygame.display.update()