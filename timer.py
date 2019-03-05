class Timer:
	def __init__(self, after, loop=True):
		self.timer = 0
		self.after = after
		self.loop = loop

	def reset(self):
		self.timer = 0

	def check(self, dt=None):
		old = self.timer
		if dt != None:
			self.timer += dt
		if old >= self.after:
			if self.loop and dt != None:
				self.timer = 0
			return True
		return False