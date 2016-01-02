import game
import primitives
from math import sin, cos
from pyglet.window import key

class Player():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.delta_alpha = 0.05
		self.alpha = 0
		self.v = 200
		self.r = 25
		self.name = 'Player'
		self.vx = 0
		self.vy = 10
	
	def update(self, dt):
		if game.keys[key.A]:
			self.alpha += self.delta_alpha
		if game.keys[key.D]:
			self.alpha -= self.delta_alpha

		self.vx = cos(self.alpha)*self.v			
		self.vy = sin(self.alpha)*self.v

		self.x += self.vx*dt
		self.y += self.vy*dt

	def render(self, cx, cy):
		primitives.circle(x=self.x, y=self.y, radius=self.r, color=(0., 0., 1., 1.))

	def add(self):
		game.player = self
		game.updates.append(self)
		game.renders.append(self)
		return self

	def remove(self):
		game.player = None
		game.updates.remove(self)
		game.renders.remove(self)
		return self