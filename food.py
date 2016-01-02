import game
import primitives
from math import sin, cos
from pyglet.window import key

game.food = []

class Food():
	def __init__(self, x, y, r):
		self.x = x
		self.y = y
		self.r = r

	def render(self, cx, cy):
		primitives.circle(x=self.x, y=self.y, radius=self.r, color=(1., 1., 1., 1.))

	def add(self):
		game.food.append(self)
		game.renders.append(self)
		return self

	def remove(self):
		game.food.remove(self)
		game.renders.remove(self)
		return self