import engine.game as game

class Event:
	def __init__(self, event=None):
		self.event = event

	def evaluate(self):
		if self.event:
			self.event()
		else: 
			raise NotImplementedError

	def add(self):
		game.events.append(self)

class AddEvent(Event):
	def __init__(self, entity):
		self.entity = entity

	def evaluate(self):
		self.entity.init()
		game.entities[self.entity.ii] = self.entity

class RemoveEvent(Event):
	def __init__(self, entity):
		self.entity = entity

	def evaluate(self):
		self.entity.outit()
		del game.entities[self.entity.ii]