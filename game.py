import pyglet
from pyglet.window import key
import struct
import threading
import sys

from engine.physics import Vec2
game = sys.modules[__name__]

def init(client=None, world=None):
	game.entities = {}
	game.groups = {}
	game.events = []
	game.time = 0

	game.low_ii = 100
	game.medium_ii = 1000
	game.high_ii = 1000000
	game.reserved_ii = {
		'camera': 5
	}

	game.mouse = Vec2(0, 0)

	game.window = None
	game.keys = None

	game.client = client
	game.world = world

	game.running = False

def loop(dt):
	#print('tick')
	events_to_handle = game.events
	game.events = []
	for event in events_to_handle:
		event.evaluate()

	if game.world:
		#timestep, velocity iter, position iter = 1/60, 6, 2
		game.world.Step(1/120, 3, 1)
		game.world.ClearForces()

	for entity in game.entities.values():
		entity.update(dt)

	game.window.clear()

	items = list(game.entities.items())
	items.sort()
	for entity in map(lambda x: x[1], items):
		entity.render()

	game.time += dt

def start():
	#samples=4
	config = pyglet.gl.Config(sample_buffers=1, samples=1)
	game.window = pyglet.window.Window(800, 600, config=config, resizable=True)

	game.keys = key.KeyStateHandler()
	game.window.push_handlers(game.keys)

	@game.window.event
	def on_mouse_motion(x, y, dx, dy):
		game.mouse.x = x
		game.mouse.y = y

	if game.client:
		game.client.init()

	pyglet.clock.schedule_interval(game.loop, 1/120.0)
	game.running = True
	pyglet.app.run()
	game.running = False

	if game.client:
		game.client.quit()


def get_ii():
	game.medium_ii += 1
	return game.medium_ii - 1

def get_low_ii():
	game.low_ii += 1
	return game.low_ii - 1

def get_high_ii():
	game.high_ii += 1
	return game.high_ii - 1
