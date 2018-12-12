import string
import math

import pyglet
from pyglet import gl

from Box2D import (b2Vec2, b2Draw)
import engine.game
from entity import Entity

import sys
this = sys.modules[__name__]
this.batch = None

class Prerender(Entity):
	def _generate_ii(self):
		return game.get_low_ii()

	def render(self):
		this.batch = pyglet.graphics.Batch()

class Postrender(Entity):
	def _generate_ii(self):
		return game.get_high_ii()

	def render(self):
		this.batch.draw()

def init():
	this.pre_render = Prerender()
	this.pre_render.add()
	this.post_render = Postrender()
	this.post_render.add()


class grBlended (pyglet.graphics.Group):
    """
    This pyglet rendering group enables blending.
    """

    def set_state(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def unset_state(self):
        gl.glDisable(gl.GL_BLEND)


class grPointSize (pyglet.graphics.Group):
    """
    This pyglet rendering group sets a specific point size.
    """

    def __init__(self, size=4.0):
        super(grPointSize, self).__init__()
        self.size = size

    def set_state(self):
        gl.glPointSize(self.size)

    def unset_state(self):
        gl.glPointSize(1.0)


class grText(pyglet.graphics.Group):
    """
    This pyglet rendering group sets the proper projection for
    displaying text when used.
    """
    window = None

    def __init__(self, window=None):
        super(grText, self).__init__()
        self.window = window

    def set_state(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.gluOrtho2D(0, self.window.width, 0, self.window.height)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()

    def unset_state(self):
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
class PygletDraw(b2Draw):
	"""
	This debug draw class accepts callbacks from Box2D (which specifies what to draw)
	and handles all of the rendering.

	If you are writing your own game, you likely will not want to use debug drawing.
	Debug drawing, as its name implies, is for debugging.
	"""
	blended = grBlended()
	circle_segments = 16
	surface = None
	circle_cache_tf = {}  # triangle fan (inside)
	circle_cache_ll = {}  # line loop (border)

	def StartDraw(self):
		pass

	def EndDraw(self):
		pass

	def triangle_fan(self, vertices):
		"""
		in: vertices arranged for gl_triangle_fan ((x,y),(x,y)...)
		out: vertices arranged for gl_triangles (x,y,x,y,x,y...)
		"""
		out = []
		for i in range(1, len(vertices) - 1):
			# 0,1,2   0,2,3  0,3,4 ..
			out.extend(vertices[0])
			out.extend(vertices[i])
			out.extend(vertices[i + 1])
		return len(out) // 2, out

	def line_loop(self, vertices):
		"""
		in: vertices arranged for gl_line_loop ((x,y),(x,y)...)
		out: vertices arranged for gl_lines (x,y,x,y,x,y...)
		"""
		out = []
		for i in range(len(vertices) - 1):
			# 0,1  1,2  2,3 ... len-1,len  len,0
			out.extend(vertices[i])
			out.extend(vertices[i + 1])

		out.extend(vertices[len(vertices) - 1])
		out.extend(vertices[0])

		return len(out) // 2, out

	def _getLLCircleVertices(self, radius, points):
		"""
		Get the line loop-style vertices for a given circle.
		Drawn as lines.

		"Line Loop" is used as that's how the C++ code draws the
		vertices, with lines going around the circumference of the
		circle (GL_LINE_LOOP).

		This returns 'points' amount of lines approximating the
		border of a circle.

		(x1, y1, x2, y2, x3, y3, ...)
		"""
		ret = []
		step = 2 * math.pi / points
		n = 0
		for i in range(points):
			ret.append((math.cos(n) * radius, math.sin(n) * radius))
			n += step
			ret.append((math.cos(n) * radius, math.sin(n) * radius))
		return ret

	def _getTFCircleVertices(self, radius, points):
		"""
		Get the triangle fan-style vertices for a given circle.
		Drawn as triangles.

		"Triangle Fan" is used as that's how the C++ code draws the
		vertices, with triangles originating at the center of the
		circle, extending around to approximate a filled circle
		(GL_TRIANGLE_FAN).

		This returns 'points' amount of lines approximating the
		circle.

		(a1, b1, c1, a2, b2, c2, ...)
		"""
		ret = []
		step = 2 * math.pi / points
		n = 0
		for i in range(points):
			ret.append((0.0, 0.0))
			ret.append((math.cos(n) * radius, math.sin(n) * radius))
			n += step
			ret.append((math.cos(n) * radius, math.sin(n) * radius))
		return ret

	def getCircleVertices(self, center, radius, points):
		"""
		Returns the triangles that approximate the circle and
		the lines that border the circles edges, given
		(center, radius, points).

		Caches the calculated LL/TF vertices, but recalculates
		based on the center passed in.

		TODO: Currently, there's only one point amount,
		so the circle cache ignores it when storing. Could cause
		some confusion if you're using multiple point counts as
		only the first stored point-count for that radius will
		show up.
		TODO: What does the previous TODO mean?

		Returns: (tf_vertices, ll_vertices)
		"""
		if radius not in self.circle_cache_tf:
			self.circle_cache_tf[
				radius] = self._getTFCircleVertices(radius, points)
			self.circle_cache_ll[
				radius] = self._getLLCircleVertices(radius, points)

		ret_tf, ret_ll = [], []

		for x, y in self.circle_cache_tf[radius]:
			ret_tf.extend((x + center[0], y + center[1]))
		for x, y in self.circle_cache_ll[radius]:
			ret_ll.extend((x + center[0], y + center[1]))
		return ret_tf, ret_ll

	def DrawCircle(self, center, radius, color):
		"""
		Draw an unfilled circle given center, radius and color.
		"""
		unused, ll_vertices = self.getCircleVertices(
			center, radius, self.circle_segments)
		ll_count = len(ll_vertices) // 2

		self.batch.add(ll_count, gl.GL_LINES, None,
					   ('v2f', ll_vertices),
					   ('c4f', [color.r, color.g, color.b, 1.0] * ll_count))

	def DrawSolidCircle(self, center, radius, axis, color):
		"""
		Draw an filled circle given center, radius, axis (of orientation) and color.
		"""
		tf_vertices, ll_vertices = self.getCircleVertices(
			center, radius, self.circle_segments)
		tf_count, ll_count = len(tf_vertices) // 2, len(ll_vertices) // 2

		self.batch.add(tf_count, gl.GL_TRIANGLES, self.blended,
					   ('v2f', tf_vertices),
					   ('c4f', [0.5 * color.r, 0.5 * color.g, 0.5 * color.b, 0.5] * tf_count))

		self.batch.add(ll_count, gl.GL_LINES, None,
					   ('v2f', ll_vertices),
					   ('c4f', [color.r, color.g, color.b, 1.0] * (ll_count)))

		p = b2Vec2(center) + radius * b2Vec2(axis)
		self.batch.add(2, gl.GL_LINES, None,
					   ('v2f', (center[0], center[1], p[0], p[1])),
					   ('c3f', [1.0, 0.0, 0.0] * 2))

	def DrawPolygon(self, vertices, color):
		"""
		Draw a wireframe polygon given the world vertices (tuples) with the specified color.
		"""
		if len(vertices) == 2:
			p1, p2 = vertices
			self.batch.add(2, gl.GL_LINES, None,
						   ('v2f', (p1[0], p1[1], p2[0], p2[1])),
						   ('c3f', [color.r, color.g, color.b] * 2))
		else:
			ll_count, ll_vertices = self.line_loop(vertices)

			self.batch.add(ll_count, gl.GL_LINES, None,
						   ('v2f', ll_vertices),
						   ('c4f', [color.r, color.g, color.b, 1.0] * (ll_count)))

	def DrawSolidPolygon(self, vertices, color):
		"""
		Draw a filled polygon given the world vertices (tuples) with the specified color.
		"""
		if len(vertices) == 2:
			p1, p2 = vertices
			self.batch.add(2, gl.GL_LINES, None,
						   ('v2f', (p1[0], p1[1], p2[0], p2[1])),
						   ('c3f', [color.r, color.g, color.b] * 2))
		else:
			tf_count, tf_vertices = self.triangle_fan(vertices)
			if tf_count == 0:
				return

			self.batch.add(tf_count, gl.GL_TRIANGLES, self.blended,
						   ('v2f', tf_vertices),
						   ('c4f', [0.5 * color.r, 0.5 * color.g, 0.5 * color.b, 0.5] * (tf_count)))

			ll_count, ll_vertices = self.line_loop(vertices)

			self.batch.add(ll_count, gl.GL_LINES, None,
						   ('v2f', ll_vertices),
						   ('c4f', [color.r, color.g, color.b, 1.0] * ll_count))

	def DrawSegment(self, p1, p2, color):
		"""
		Draw the line segment from p1-p2 with the specified color.
		"""
		self.batch.add(2, gl.GL_LINES, None,
					   ('v2f', (p1[0], p1[1], p2[0], p2[1])),
					   ('c3f', [color.r, color.g, color.b] * 2))

	def DrawXForm(self, xf):
		"""
		Draw the transform xf on the screen
		"""
		p1 = xf.position
		k_axisScale = 0.4
		p2 = p1 + k_axisScale * xf.R.x_axis
		p3 = p1 + k_axisScale * xf.R.y_axis

		self.batch.add(3, gl.GL_LINES, None,
					   ('v2f', (p1[0], p1[1], p2[0], p2[
						1], p1[0], p1[1], p3[0], p3[1])),
					   ('c3f', [1.0, 0.0, 0.0] * 2 + [0.0, 1.0, 0.0] * 2))

	def DrawPoint(self, p, size, color):
		"""
		Draw a single point at point p given a point size and color.
		"""
		self.batch.add(1, gl.GL_POINTS, grPointSize(size),
					   ('v2f', (p[0], p[1])),
					   ('c3f', [color.r, color.g, color.b]))

	def DrawAABB(self, aabb, color):
		"""
		Draw a wireframe around the AABB with the given color.
		"""
		self.renderer.batch.add(8, gl.GL_LINES, None,
								('v2f', (aabb.lowerBound.x, aabb.lowerBound.y,
										 aabb.upperBound.x, aabb.lowerBound.y,
										 aabb.upperBound.x, aabb.lowerBound.y,
										 aabb.upperBound.x, aabb.upperBound.y,
										 aabb.upperBound.x, aabb.upperBound.y,
										 aabb.lowerBound.x, aabb.upperBound.y,
										 aabb.lowerBound.x, aabb.upperBound.y,
										 aabb.lowerBound.x, aabb.lowerBound.y)),
								('c3f', [color.r, color.g, color.b] * 8))

	def to_screen(self, point):
		"""
		In here for compatibility with other frameworks.
		"""
		return tuple(point)

b2draw = PygletDraw()