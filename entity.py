import engine.game as game
from engine.event import AddEvent, RemoveEvent

class Entity:
	def __init__(self):
		self.ii = self.generate_ii()

	def generate_ii(self):
		return game.get_ii()

	def init(self):
		pass

	def render(self):
		pass

	def update(self, dt):
		pass

	def outit(self):
		pass

	def add(self):
		AddEvent(self).add()

	def remove(self):
		RemoveEvent(self).add()

