import engine.game as game
from engine.event import AddEvent, RemoveEvent

class Entity:
	def generate_iid(self):
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
		self.iid = self.generate_iid()
		AddEvent(self).add()

	def remove(self):
		RemoveEvent(self).add()
