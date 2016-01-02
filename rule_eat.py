import game
from math import sqrt
import sys

def update(dt):
	if not game.player or not game.food:
		return

	player = game.player
	for food in game.food:
		dx = food.x - player.x
		dy = food.y - player.y
		if sqrt(dx*dx + dy*dy) < player.r + food.r:
			player.r += food.r
			food.remove()

def add():
	game.updates.append(sys.modules[__name__])

def remove():
	game.updates.remove(sys.modules[__name__])