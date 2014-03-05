from path_finder import find_path
import numpy
import pygame

class staticObject():
    def __init__(self, name, (x,y), id, graphic = ""):
        self.positionX = x  # aktualna pozycja obiektu
        self.positionY = y
        self.name = name  # nazwa obiektu
        self.sourceGraphic = graphic
        self.id = id
        self.visible = 0

    def __str__(self):
        return self.name

    def getGraphic(self):
        return self.sourceGraphic

    def getName(self):
        return self.name

    def getPosition(self):
        return (self.positionX, self.positionY)

    # ustawienie aktualnej pozycji obiektu
    def setPosition(self, (x, y)):
        self.positionX = int(x)
        self.positionY = int(y)


class dynamicObject(staticObject):

    def __init__(self, name, (x, y), graphic = "", step = 1):
        self.positionX = x  # aktualna pozycja obiektu
        self.positionY = y
        self.name = name  # nazwa obiektu
        self.targetX = self.positionX  # cel do ktorego zmierza obiekt
        self.targetY = self.positionY
        self.bufTargetX = -1
        self.bufTargetY = -1
        self.moving = 0
        self.doorFlag = 0
        self.path =[]
        self.sourceGraphic = 'images/edit_table1.png'
        self.step = step  # krok / predkosc z jakas sie przemieszcza, domyslnie ustawiona na 1

    # ustawiamy cel naszego obiektu
    # jesli cel != aktualna pozycja - metoda move
    # zacznie przemieszczac obiekt
    def setTarget(self, tarX, tarY):
        self.targetX = tarX
        self.targetY = tarY

    def getTarget(self):
        return (self.targetX , self.targetY)

    def setStep(self, step):
        self.step = step

    def getDirection(self):
        return self.direction

    # jesli podamy parametr predkosci, to zostanie on zapamietany i wykorzystany
    # w ruchu, wpw move bedzie korzystac z zapamietanego kroku 'step'

    def move(self, matrix = [], data = [] , step = 1 ):

        targetX = self.targetX
        targetY = self.targetY

        currentX = self.positionX
        currentY = self.positionY

        def heroCollisionCheck(x, y): # funkcja sprawdzajaca, czy mozna wejsc na dane pole
            return matrix[x,y]

        def animateHeroMovement(x0, y0, x, y): # funkcja ruchu

            d = numpy.sqrt((x-x0)*(x-x0)+(y-y0)*(y-y0)) # wyznaczamy odleglosc miedzy punktami
            if ((x-x0) != 0):
                a = numpy.arctan(numpy.fabs(y-y0)/numpy.fabs(x-x0)) # kat nachylenia wzgledem prostej OX
            else:
                a = 0

            # i zwiekszamy o krok do czasu gdy nie osiagnie wartosci d (odleglosc miedzy punktami)
            # jednoczesnie obliczajac wspolrzedne nowych punktow

            if ( x > x0 ):
                if ( y < y0 ):
                    newx = x - (d - self.step)*numpy.cos(a)
                    newy = y + (d - self.step)*numpy.sin(a)
                else:
                    newx = x - (d - self.step)*numpy.cos(a)
                    newy = y - (d - self.step)*numpy.sin(a)
            else:
                if ( y < y0 ):
                    newx = x + (d - self.step)*numpy.cos(a)
                    newy = y + (d - self.step)*numpy.sin(a)
                else:
                    newx = x + (d - self.step)*numpy.cos(a)
                    newy = y - (d - self.step)*numpy.sin(a)

            if ( heroCollisionCheck(newx, newy) > 0 ): # jak nie ma kolizji to updatujemy nowa pozycje dla obiektu
                self.positionX = newx
                self.positionY = newy
                return 0
            else:
                return -1

        if ( self.positionX == self.targetX and self.positionY == self.targetY ): # jesli jestesmy na miejscu nie robimy nic i upewniamy sie, ze zmienne sa
            self.doorFlag = 0                                                     # w stanie poczatkowym
            self.bufTargetX = -1
            self.bufTargetY = -1
            self.path = []
            self.moving = 0
            self.direction = [0,0]
            return 0
        else:
            self.moving = 1
            targetChamber = heroCollisionCheck(targetX, targetY)
            currentChamber = heroCollisionCheck(currentX, currentY)

            if targetChamber > 0: # wykluczenie przypadkow wychodzenia poza mape
                if ( targetChamber == currentChamber ): # przypadek kiedy jestesmy w tym samym pomieszczeniu
                    self.bufTargetX = -1
                    self.bufTargetY = -1
                    animateHeroMovement(currentX, currentY, targetX, targetY) # wywolanie funkcji ruchu
                else: # przypadek gdy jestesmy w innym pokoju
                    if self.doorFlag != 1: # jesli nie jestesmy w drzwiach (miedzy dwoma punktami we i wy)
                        self.path = find_path(int(currentChamber),int(targetChamber),data) # wyszukujemy sciezke do celu
                    # jesli jestesmy w punkcie we drzwi ustawiamy flage drzwi na 1
                    if ( numpy.fabs(currentX - int(self.path[0][0][0][0])) < 1 ) and ( numpy.fabs(currentY - int(self.path[0][0][0][1])) < 1 ):
                        self.doorFlag = 1
                    # jesli jestesmy w punkcie wy drzwi ustawiamy flage drzwi na 0
                    if ( numpy.fabs(currentX - int(self.path[0][0][1][0])) < 1 ) and ( numpy.fabs(currentY - int(self.path[0][0][1][1])) < 1 ):
                        self.doorFlag = 0

                    self.bufTargetX = int(self.path[0][0][self.doorFlag][0]) # ustawiamy buforowe cele na wspolrzedne drzwi
                    self.bufTargetY = int(self.path[0][0][self.doorFlag][1])
                    animateHeroMovement(currentX, currentY, self.bufTargetX , self.bufTargetY) # i ruszamy do tego celu

            if ( numpy.fabs(self.targetX-self.positionX) < self.step and numpy.fabs(self.targetY-self.positionY) < self.step ): # jesli sie znajdujemy w poblizu punktu docelowego
                self.positionX = self.targetX # ustaiwamy wspolrzedne na ten punkt
                self.positionY = self.targetY

        return self.moving



if __name__ == "__main__":
	
	npc = gameObject('Stworek', (1,2))
	print npc
	print npc.getPosition()
	npc.setPosition((3,4))
	print npc.getPosition()
	npc.setTarget(5,6)
	npc.move()