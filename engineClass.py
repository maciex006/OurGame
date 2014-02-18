class gameObject:

	def __init__(self, name, (x, y)):
		self.position = (x, y)
		self.name = name

	def __str__(self):
		return self.name

	def getPosition(self):
		return self.position

	def move(self, x0, y0, x1, y1):
		pass

if __name__ == "__main__":
	
	npc = gameObject('Stworek', (1,2))
	print npc
	print npc.getPosition()