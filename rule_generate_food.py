import game
from food import Food
from random import random
import sys

spawn = 0
def update(dt):
	global spawn
	spawn += dt
	if spawn > 0.5:
		Food(random()*game.window.width, random()*game.window.height, random()*3 + 2).add()
		spawn = 0


def add():
	game.updates.append(sys.modules[__name__])

def remove():
	game.updates.remove(sys.modules[__name__])