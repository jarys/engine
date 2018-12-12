from engine import game
from pyglet.text import Label
from engine.event import Event
from engine.entity import Entity
label = Label('Hello, world',
				font_name='Consolas',
				font_size=36,
				x=0, y=0)

from pyglet.gl import glMatrixMode, glLoadIdentity, gluOrtho2D
from pyglet.gl import GL_PROJECTION, GL_MODELVIEW, glPopMatrix

def init():
	@game.window.event
	def on_draw():
		label.draw()

class Terminal(Entity):
	def render(self):
		label.draw()

	def generate_ii(self):
		return 1

Terminal().add()

'''def add():
	Event(init).add()

add()'''