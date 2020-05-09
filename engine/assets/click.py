import game
from circle import Circle
import sys
import hexgrid

added = []
event = False
def update(dt):
	global event
	if not event:
		@game.window.event
		def on_mouse_press(x, y, button, modifiers):
		    gx, gy = hexgrid.grid(x + game.cx - game.dcx, y + game.cy - game.dcy, 50)
		    if (gx, gy) not in added:
		    	x, y = hexgrid.pos(gx, gy, 50)
		    	Circle.new(x, y, 50)
		    	added.append((gx, gy))
		event = True

def add():
	game.updates.append(sys.modules[__name__])

def remove():
	game.updates.remove(sys.modules[__name__])