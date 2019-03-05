from constants import *
from timer import *

class Piece:
	def __init__(self, field, type, x=None, y=None):
		self.type = type
		self.field = field
		self.shape = Shapes[self.type]
		self.size = len(self.shape)
		if x != None:
			self.x = x
			self.y = y
		else:
			self.x = self.field.width // 2 - self.size // 2
			self.y = 1

		self.rotation = 0

		self.hasSet = False
		# these are all in seconds
		self.setT = Timer(1, loop=False)
		self.fallT = Timer(1)
		self.softDropT = Timer(0.01)

		self.dasT = Timer(180/1000, loop=False)
		self.arrT = Timer(-1)

		updateColors(self.field.screen)

	def rotate(self, dir):
		newShape = [[0 for _ in range(self.size)] for _ in range(self.size)]
		for y in range(self.size):
			for x in range(self.size):
				if self.shape[y][x] == 1:
					if dir == 'left':
						newShape[self.size - 1 - x][y] = 1
					elif dir == 'right':
						newShape[x][self.size - 1 - y] = 1

		oldShape = self.shape
		self.shape = newShape

		prevRot = self.rotation
		self.rotation = (self.rotation + (1 if dir == 'right' else -1)) % 4

		wallkick = Wallkick.get(self.type)
		if wallkick == None: wallkick = Wallkick['default']

		testOffset = (2 * prevRot + (0 if dir == 'right' else -1)) % 8
		for test in wallkick:
			offset = test[testOffset]
			if not self.collides(None, *offset):
				self.x += offset[0]
				self.y += offset[1]
				return
		self.shape = oldShape
		self.rotation = prevRot

	def collides(self, dir=None, xOff=None, yOff=None):
		if xOff == None:
			xOff, yOff = 0, 0
			if dir == 'down': xOff, yOff = 0, 1
			if dir == 'left': xOff, yOff = -1, 0
			if dir == 'right': xOff, yOff = 1, 0

		for i in range(self.size):
			for j in range(self.size):
				if self.shape[j][i]:
					x = i + self.x + xOff
					y = j + self.y + yOff
					if self.field.outside(x,y):
						return True
					if self.field.getCell(x, y):
						return True

		return False

	def move(self, dir):
		xOff, yOff = 0, 0
		if dir == 'down': xOff, yOff = 0, 1
		if dir == 'left': xOff, yOff = -1, 0
		if dir == 'right': xOff, yOff = 1, 0

		if not self.collides(dir):
			self.x += xOff
			self.y += yOff
			return True

		return False

	def update(self, key, dt):
		if self.field.Input.pressed('hardDrop'):
			while self.move('down'): pass
			self.set()

		if self.field.Input.down('softDrop'):
			if self.softDropT.check(dt):
				self.move('down')

		if self.field.Input.down('left') and not self.field.Input.pressed('right'):
			if self.field.Input.pressed('left'): self.dasT.reset()
			das = self.dasT.check(dt)
			if das and self.arrT.after == -1: 
				while self.move('left'): pass
			elif self.field.Input.pressed('left') or (das and self.arrT.check(dt)):
				self.move('left')

		elif self.field.Input.down('right') and not self.field.Input.pressed('left'):
			if self.field.Input.pressed('right'): self.dasT.reset()
			das = self.dasT.check(dt)
			if das and self.arrT.after == -1: 
				while self.move('right'): pass
			elif self.field.Input.pressed('right') or (das and self.arrT.check(dt)):
				self.move('right')

		else:
			self.dasT.reset()
			self.arrT.reset()

		if self.field.Input.pressed('rotateCcw'):
			self.rotate('left')
		if self.field.Input.pressed('rotateCw'):
			self.rotate('right')

		if self.collides('down'):
			if self.setT.check(dt) and not self.hasSet:
				self.set()
		else:
			if self.fallT.check(dt):
				self.move('down')

	def set(self):
		for y in range(self.size):
			for x in range(self.size):
				if self.shape[y][x] == 1:
					self.field.setCell(self.x + x, self.y + y, self.type)
		self.hasSet = True

	def show(self):
		screen = self.field.screen

		oldY = self.y
		while self.move('down'): pass
		hardDropY = self.y
		self.y = oldY

		for y in range(self.size):
			for x in range(self.size):
				if self.shape[y][x] == 0:
					continue
				# draw ghost
				c = Colors.get(self.type+'Ghost')
				if c == None: c = Colors[self.type]
				screen.print_at(' '*2, self.x * 2 + self.field.x + x * 2, hardDropY + self.field.y + y - self.field.hidden,
								bg=c)

				screen.print_at(' '*2, self.x * 2 + self.field.x + x * 2, self.y + self.field.y + y - self.field.hidden,
								bg=Colors[self.type])

