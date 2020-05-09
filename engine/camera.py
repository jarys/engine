from engine.physics import Vec2
from pyglet.gl import glMatrixMode, glLoadIdentity, gluOrtho2D
from pyglet.gl import GL_PROJECTION, GL_MODELVIEW
import engine.game as game
from engine.entity import Entity

class Camera(Vec2, Entity):
	def __init__(self, pos=(0, 0), zoom=0.25):
		#possible inheritance fail
		Vec2.__init__(self, pos[0], pos[1])
		Entity.__init__(self)

		self.zoom = zoom
		self.shift = Vec2(0, 0)

	def _generate_ii(self):
		return game.get_low_ii()

	def update(self, dt):
		self.shift.x = game.window.width*0.5
		self.shift.y = game.window.height*0.5

	def render(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluOrtho2D(*self.rect())
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def rect(self):
		'''	a      b
			|      |
		c --+------+--
			|      |
		d --+------+--
			|      |  '''
		return (self.x - self.shift.x*self.zoom,
				self.x + self.shift.x*self.zoom,
				self.y - self.shift.y*self.zoom,
				self.y + self.shift.y*self.zoom)

	def init(self):
		game.camera = self

	def outit(self):
		del game.camera

	def click_transform(self, click):
		return self + self.zoom*(click - self.shift)


