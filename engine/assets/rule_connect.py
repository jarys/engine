import game
import sys
import itertools
import primitives
import math

from firefly import Firefly
from entity import Entity

class RuleConnect(Entity):
	def render(self):
		if not Firefly in game.groups.keys():
			return

		for m, f in itertools.combinations(game.groups[Firefly], 2):
			d = (m.pos - f.pos).length
			if d < 10:
				c = math.sqrt(10 - d)
				primitives.line(a=m.pos, b=f.pos, color=4*(c/10,), stroke=10*c)


def add():
	RuleConnect().add()
