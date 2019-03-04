from random import shuffle
from piece import *
from constants import *

class Field:
	def __init__(self, screen, Input=None):
		self.screen = screen
		self.Input = Input
		self.width = 10
		self.height = 20
		self.hidden = 2
		self.grid = [None for _ in range((self.height + self.hidden) * self.width)]
		self.x = screen.width // 2 - self.width
		self.y = 2

		self.pieces = list('IJLOSTZ')
		self.bag = []
		self.upcoming = []

		self.newActive()

		self.held = None
		self.hasHeld = False
		self.lines = 0

		updateColors(self.screen)

	def outside(self, x, y):
		return x < 0 or x >= self.width or y < 0 or y >= self.height + self.hidden

	def getCell(self, x, y):
		if self.outside(x,y): return
		return self.grid[y * self.width + x]

	def setCell(self, x, y, cell):
		if self.outside(x,y): return
		self.grid[y * self.width + x] = cell

	def getUpcoming(self, remove=False, n=1):
		while len(self.upcoming) < n:
			if len(self.bag) == 0:
				shuffle(self.pieces)
				self.bag = self.pieces.copy()
			self.upcoming.append(self.bag.pop(0))
		if n == 1:
			if remove:
				return self.upcoming.pop(0)
			return self.upcoming[0]
		else:
			pieces = self.upcoming[:n]
			if remove:
				for _ in range(n):
					self.upcoming.pop(0)
			return pieces	


	def newActive(self, type=None):
		if type == None:
			type = self.getUpcoming(True)
		self.active = Piece(self, type)

	def clearLines(self):
		for y in range(self.height + self.hidden):#range(self.height + self.hidden - 1, 0, -1):
			if all(self.grid[y * self.width : (y + 1) * self.width]):
				self.lines += 1
				self.move('down', y)

	def move(self, dir, yOff=None):
		if yOff == None: yOff = self.height + self.hidden
		if dir == 'down':
			for y in range(yOff, 0, -1):
				for x in range(self.width):
					if y == 0:
						self.setCell(x, y, None)
					else:
						self.setCell(x, y, self.getCell(x, y - 1))

	def update(self, key, dt):
		self.active.update(key, dt)
		if self.active.hasSet:
			self.clearLines()
			self.newActive()
			self.hasHeld = False
		if key in (ord('c'),ord('C')) and not self.hasHeld:
			self.hasHeld = True
			old = self.active.type
			self.newActive(self.held)
			self.held = old

	def show(self):
		for y in range(self.height):
			for x in range(self.width):
				c = ' '
				tiles = ['│','─','┌','┐','└','┘']
				if x == 0:
					if y == 0: c = tiles[2]
					elif y == self.height - 1: c = tiles[4]
					else: c = tiles[0]
				elif x == self.width - 1:
					if y == 0: c = tiles[3]
					elif y == self.height - 1: c = tiles[5]
					else: c = tiles[0]
				elif y == 0 or y == self.height - 1:
					c = tiles[1]

				cell = self.getCell(x, y + self.hidden)
				bg = Colors[cell] if cell != None else 0
				if cell != None: c = ' '

				tmp = tiles[1] if y == 0 or y == self.height - 1 and cell == None else ' '
				if x == 0: c += tmp
				elif x == self.width - 1: c = tmp + c
				else: c = c*2
				self.screen.print_at(c, x * 2 + self.x, y + self.y, bg=bg)

		self.active.show()

		# upcoming
		yOff = 0
		for p in self.getUpcoming(False, 5):
			shape = Shapes[p]
			xOff = self.screen.width // 2 + self.width
			for y, row in enumerate(shape):
				for x, cell in enumerate(row):
					if cell == 1:
						self.screen.print_at(' '*2, x*2 + xOff + 1, y + yOff + self.y, bg=Colors[p])
			yOff += len(shape)
			if p == 'O': yOff += 1

		# held
		if self.held:
			shape = Shapes[self.held]
			xOff = self.screen.width // 2 - self.width - len(shape) - 4
			for y, row in enumerate(shape):
				for x, cell in enumerate(row):
					if cell == 1:
						self.screen.print_at(' '*2, x * 2 + xOff, y + self.y, bg=Colors[self.held])
