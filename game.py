import pyglet
from pyglet.window import key
import primitives

config = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(800, 600, config=config, resizable=True)

keys = key.KeyStateHandler()
window.push_handlers(keys)

updates = []
renders = []
time = 0
cx, cy = 0, 0

def loop(dt):
	global time

	for entity in updates:
		entity.update(dt)

	window.clear()
	for entity in renders:
		entity.render(cx, cy)

	time += dt

def run():
	pyglet.clock.schedule_interval(loop, 1/120.0)
	pyglet.app.run()