import engine.game as game
import sys
from pyglet.window import key

class EntityControl:
	def __init__(self, entity):
		self.entity = entity

	def update(self, dt):
			if game.keys[key.W]:
				if self.entity.v < 200:
					self.entity.v += 10
			else:
				if self.entity.v > 0:
					self.entity.v -= 10
			if game.keys[key.A]:
				self.entity.alpha += self.entity.delta_alpha
			if game.keys[key.D]:
				self.entity.alpha -= self.entity.delta_alpha

			game.cx = self.entity.x
			game.cy = self.entity.y

	def add(self):
		game.updates.append(self)

	def remove(self):
		game.updates.remove(self)