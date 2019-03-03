from constants import *
import Input

Input.bind('left', 'left')
Input.bind('right', 'right')
Input.bind('down', 'softDrop')
Input.bind('up', 'hardDrop')
Input.bind('x', 'rotateCw')
Input.bind('z', 'rotateCcw')
Input.bind('c', 'hold')

class Timer:
	def __init__(self, after, loop=True):
		self.timer = 0
		self.after = after
		self.loop = loop

	def reset(self):
		self.timer = 0

	def check(self, add=True):
		old = self.timer
		if add:
			self.timer += 1
		if old >= self.after:
			if self.loop and add:
				self.timer = 0
			return True
		return False

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
		# these are all in frames and not in seconds
		self.setT = Timer(120, loop=False)
		self.fallT = Timer(60)
		self.softDropT = Timer(5)

		self.dasT = Timer(30, loop=False)
		self.arrT = Timer(0)

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

	def update(self, key):
		Input.update()

		if Input.pressed('hardDrop'):
			while self.move('down'): pass
			self.set()

		if Input.down('softDrop'):
			if self.softDropT.check():
				self.move('down')

		if Input.down('left') or Input.down('right'):
			das = self.dasT.check()
			arr = self.arrT.check()
		else:
			self.dasT.reset()
			self.arrT.reset()

		if Input.pressed('left') or (Input.down('left') and das and arr):
			if das and self.arrT.after == -1: 
				while self.move('left'): pass
			else: self.move('left')
		if Input.pressed('right') or (Input.down('right') and das and arr):
			if das and self.arrT.after == -1: 
				while self.move('right'): pass
			else: self.move('right')

		if Input.pressed('rotateCcw'):
			self.rotate('left')
		if Input.pressed('rotateCw'):
			self.rotate('right')

		if self.collides('down'):
			if self.setT.check() and not self.hasSet:
				self.set()
		else:
			if self.fallT.check():
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
				screen.print_at(' ', self.x + self.field.x + x, hardDropY + self.field.y + y - self.field.hidden,
								bg=Colors[self.type])

				screen.print_at(' ', self.x + self.field.x + x, self.y + self.field.y + y - self.field.hidden,
								bg=Colors[self.type])

