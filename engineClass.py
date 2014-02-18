from path_finder import find_path
import numpy
import pygame

class gameObject():

	def __init__(self, name, (x, y), step = 1):
		self.positionX = x  # aktualna pozycja obiektu
		self.positionY = y
		self.name = name  # nazwa obiektu
		self.targetX = self.positionX  # cel do ktorego zmierza obiekt
		self.targetY = self.positionY
		self.bufTargetX = -1
		self.bufTargetY = -1
 		self.doorFlag = 0
		self.roomFlag = 0
		self.step = step  # krok / predkosc z jakas sie przemieszcza, domyslnie ustawiona na 1

	def __str__(self):
		return self.name

	def getName(self):
		return self.name

	def getPosition(self):
		return (self.positionX, self.positionY)

	# ustawienie aktualnej pozycji obiektu
	def setPosition(self, (x, y)):
		self.positionX = int(x)
		self.positionY = int(y)

	# ustawiamy cel naszego obiektu
	# jesli cel != aktualna pozycja - metoda move
	# zacznie przemieszczac obiekt
	def setTarget(self, tarX, tarY):
		self.targetX = tarX
		self.targetY = tarY

	def setStep(self, step):
		self.step = step

	# jesli podamy parametr predkosci, to zostanie on zapamietany i wykorzystany
	# w ruchu, wpw move bedzie korzystac z zapamietanego kroku 'step'
	def move1(self, step = -1):
		if step != -1:
			self.setStep(step)
		#print "cel to: (", x, ",", y, ")"
		if self.positionX != self.targetX:
			if self.positionX < self.targetX:
				self.positionX += self.step
			else:
				self.positionX -= self.step
		if self.positionY != self.targetY:
			if self.positionY < self.targetY:
				self.positionY += self.step
			else:
				self.positionY -= self.step

		return self.getPosition()

	def move(self, matrix = [], data = [] , step = -1):

		targetX = self.targetX
		targetY = self.targetY

		currentX = self.positionX
		currentY = self.positionY

		def heroCollisionCheck(x, y):
			return matrix[x,y]

		def animateHeroMovement(x0, y0, x, y):

			d = numpy.sqrt((x-x0)*(x-x0)+(y-y0)*(y-y0))
			if ((x-x0) != 0):
				a = numpy.arctan(numpy.fabs(y-y0)/numpy.fabs(x-x0))
			else:
				a = 0

			new_d = -step

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

				print(newx)
				print(newy)

				if heroCollisionCheck(newx, newy):
					self.positionX = newx
					self.positionY = newy
					return 0
				else:
					return -1

		targetChamber = heroCollisionCheck(targetX, targetY)
		currentChamber = heroCollisionCheck(currentX, currentY)

		if targetChamber != 0:
			if ( targetChamber == currentChamber ):
				self.bufTargetX = -1
				self.bufTargetY = -1
				print( "pozycja1:" + str(currentX) + "," +str(currentY))
				print( "cel1:" + str(targetX) + "," +str(targetY))
				animateHeroMovement(currentX, currentY, targetX, targetY)
				#return self.getPosition()

			else:
				print(currentChamber)
				path = find_path(int(currentChamber),int(targetChamber),data)
				print(path)
				#for i in range( len(path[0])):
				if ( numpy.fabs(currentX - int(path[0][self.roomFlag][0][0])) < 1 ) and ( numpy.fabs(currentY - int(path[0][self.roomFlag][0][1])) < 1 ):
					self.doorFlag = 1
				if ( numpy.fabs(currentX - int(path[0][self.roomFlag][1][0])) < 1 ) and ( numpy.fabs(currentY - int(path[0][self.roomFlag][1][1])) < 1 ):
					self.doorFlag = 0
					self.roomFlag = self.roomFlag+1

				self.bufTargetX = int(path[0][self.roomFlag][self.doorFlag][0])
				self.bufTargetY = int(path[0][self.roomFlag][self.doorFlag][1])

				print( "pozycja2:" + str(currentX) + "," +str(currentY))
				print( "cel2:" + str(self.bufTargetX) + "," +str(self.bufTargetY))

				animateHeroMovement(currentX, currentY, self.bufTargetX , self.bufTargetY)

				targetX = self.bufTargetX
				targetY = self.bufTargetY
				print( "pozycja3:" + str(currentX) + "," +str(currentY))
				print( "cel3:" + str(self.bufTargetX) + "," +str(self.bufTargetY))
				animateHeroMovement(currentX, currentY , targetX , targetY)


		if ( numpy.fabs(self.targetX-self.positionX) < 1 and numpy.fabs(self.targetY-self.positionY) < 1 ):
			self.positionX = self.targetX
			self.positionY = self.targetY
			self.roomFlag = 0

		return self.getPosition()



if __name__ == "__main__":
	
	npc = gameObject('Stworek', (1,2))
	print npc
	print npc.getPosition()
	npc.setPosition((3,4))
	print npc.getPosition()
	npc.setTarget(5,6)
	npc.move()