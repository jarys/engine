import engine.game as game
import sys
from pyglet.window import key
from engine.entity import Entity

shift = 20

class CameraControl(Entity):
	def init(self):
		game.window.push_handlers(self.on_mouse_scroll)

	def update(self, dt):
		cdelta = shift*game.camera.zoom
		if game.keys[key.W]:
			game.camera.y += cdelta
		if game.keys[key.S]:
			game.camera.y -= cdelta
		if game.keys[key.A]:
			game.camera.x -= cdelta
		if game.keys[key.D]:
			game.camera.x += cdelta

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
	    game.camera.zoom *= 1.10**(-scroll_y)
	    #print('zoom', game.camera.zoom)

def add():
	CameraControl().add()
