import online

@online.online()
class Point:
	@online.online("Point")
	def __init__(self, x, y):
		self.x = x
		self.y = y

	@online.online()
	def move(self):
		self.x += 1
		self.y += 1

	def __repr__(self):
		return str(self)
	def __str__(self):
		return f"Point({self.x},{self.y})"
	def __del__(self):
		print("del")
		super().__del__()

online.client.connect()
online.client.start()
#online.client.close()