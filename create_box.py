__author__ = 'maciex'

import numpy

a = (192,249)
b = (361,205)
d = (385,460)
c = (591,383)

DIM_X =  700
DIM_Y =  700

POINTS = ( a , b , c , d)

def create_box ( DIM_X , DIM_Y , POINTS ):
    matrix = numpy.zeros(shape=(DIM_X,DIM_Y))




    def solve( (x1 , y1) , (x2 , y2) ):
        ARRAY_1 = numpy.array([[x1,1], [x2,1]])
        ARRAY_2 = numpy.array([y1,y2])
        return numpy.linalg.solve(ARRAY_1, ARRAY_2)

    line1 = solve( POINTS[0] , POINTS[1] )
    line2 = solve( POINTS[1] , POINTS[2] )
    line3 = solve( POINTS[2] , POINTS[3] )
    line4 = solve( POINTS[3] , POINTS[0] )

    for i in range(a[0],b[0]):
        for j in range(0,DIM_Y):
            if ( ( j < line1[0]*i + line1[1]) and ( j > line2[0]*i + line2[1] ) ):
                matrix[i,j] = 1

    for i in range(b[0],c[0]):
        for j in range(0,DIM_Y):
            if ( ( j < line1[0]*i + line1[1]) and ( j > line4[0]*i + line4[1] ) ):
                matrix[i,j] = 1

    for i in range(c[0],d[0]):
        for j in range(0,DIM_Y):
            if ( ( j < line3[0]*i + line3[1]) and ( j > line4[0]*i + line4[1] ) ):
                matrix[i,j] = 1

    return matrix