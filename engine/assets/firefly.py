import game
import primitives
import random
from math import sin, cos
from physics import Vec2
from entity import Entity


class Firefly(Entity):
	def __init__(self, x, y):
		super().__init__()
		self.body = game.world.CreateDynamicBody(position=(x, y))
		self.pos = self.body.position
		self.r = 1
		self.alfa = random.random()*100
		self.speed = 0

	def update(self, dt):
		self.speed += (random.random() - 0.5)*5*dt
		self.alfa  += (random.random() - 0.5)*dt
		force = Vec2(cos(self.alfa)*cos(self.speed),
					 sin(self.alfa)*cos(self.speed))*10
		self.body.linearVelocity = force

		if self.pos.x > 50:
			self.pos.x -= 100
		if self.pos.x < -50:
			self.pos.x += 100
		if self.pos.y > 40:
			self.pos.y -= 80
		if self.pos.y < -40:
			self.pos.y += 80

	def render(self):
		primitives.circle(self.pos, self.r, color=4*(.7,))

	def init(self):
		myclass = self.__class__
		if myclass in game.groups.keys():
			game.groups[myclass].append(self)
		else:
			game.groups[myclass] = [self]

	def outit(self):
		pass
		#remove from group
