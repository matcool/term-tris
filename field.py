from random import shuffle
from piece import *
from constants import *
from helpers import *

class Field:
	def __init__(self, screen, Input=None, basic=False):
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

		self.setAfter = 1
		self.gravity = 1
		self.softDropAfter = 0.01

		self.das = 180/1000
		self.arr = -1

		self.level = 1
		self.score = 0
		self.combo = -1


		if not basic:
			self.newActive()

		self.held = None
		self.hasHeld = False
		self.lines = 0

		self.basic = basic

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
		prevGrid = self.grid.copy()
		prevLines = self.lines
		for y in range(self.height + self.hidden):#range(self.height + self.hidden - 1, 0, -1):
			if all(self.grid[y * self.width : (y + 1) * self.width]):
				self.lines += 1
				self.move('down', y)
		self.updateScore(prevGrid, prevLines)

	def updateScore(self, grid, lines):
		index = lambda x,y: grid[y * self.width + x] if not self.outside(x,y) else None
		cleared = self.lines - lines
		if cleared == 0:
			self.combo = -1
		else:
			self.combo += 1
			self.score += 50 * self.combo * self.level
		corners = sum((index(self.active.x, self.active.y) != None,
					  index(self.active.x + 2, self.active.y) != None,
					  index(self.active.x, self.active.y + 2) != None,
					  index(self.active.x + 2, self.active.y + 2) != None))
		if self.active.type == 'T' and corners >= 3:
			scores = [400, 800, 1200, 1600]
			self.score += scores[cleared] * self.level
		else:
			scores = [0, 100, 300, 500, 800]
			self.score += scores[cleared] * self.level
		


	def move(self, dir, yOff=None):
		if yOff == None: yOff = self.height + self.hidden
		if dir == 'down':
			for y in range(yOff, 0, -1):
				for x in range(self.width):
					if y == 0:
						self.setCell(x, y, None)
					else:
						self.setCell(x, y, self.getCell(x, y - 1))
		elif dir == 'up':
			for y in range(0, yOff):
				for x in range(self.width):
					if y == self.height + self.hidden:
						self.setCell(x, y, None)
					else:
						self.setCell(x, y, self.getCell(x, y + 1))

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
		fancyRect(self.screen,self.x,self.y,self.width*2-1,self.height-1)
		for y in range(self.height):
			for x in range(self.width):
				c = ' '

				cell = self.getCell(x, y + self.hidden)
				if cell != None:
					bg = Colors[cell]
					c = '▒' if self.screen.colours == 8 and cell == 'L' else ' '
					self.screen.print_at(c*2, x * 2 + self.x, y + self.y, bg=bg, colour=1)

		if not self.basic:
			self.active.show()
			self.screen.print_at(str(self.score),0,0)

			# upcoming
			yOff = 0
			for p in self.getUpcoming(False, 5):
				shape = Shapes[p]
				xOff = self.x + self.width * 2
				for y, row in enumerate(shape):
					for x, cell in enumerate(row):
						if cell == 1:
							self.screen.print_at(' '*2, x*2 + xOff + 1, y + yOff + self.y, bg=Colors[p])
				yOff += len(shape)
				if p == 'O': yOff += 1

			# held
			if self.held:
				shape = Shapes[self.held]
				xOff = self.x - len(shape) - 4
				for y, row in enumerate(shape):
					for x, cell in enumerate(row):
						if cell == 1:
							self.screen.print_at(' '*2, x * 2 + xOff, y + self.y, bg=Colors[self.held])
