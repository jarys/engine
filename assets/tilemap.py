import game
from entity import Entity
import primitives
from b2draw import b2draw
from pyglet import image

from Box2D import b2BodyDef, b2Body, b2PolygonShape
from Box2D import b2FixtureDef, b2_staticBody

from PIL import Image

class TileMap(Entity):
	boxShape = b2PolygonShape()
	boxShape.SetAsBox(1, 1)
	boxFixtureDef = b2FixtureDef(
		shape=boxShape,
		density=1
		)
	def __init__(self, pos=(0, 0), size=(10, 10)):
		super().__init__()
		self.pos = pos
		#self.size = size
		raw = Image.open('q4_map.png')
		pixels = raw.load()
		self.size = raw.width, raw.height
		self.blocks = dict()
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				if pixels[x, y][3] == 0:
					self.blocks[x, y] = None
				else:
					self.blocks[x, y] = SolidBlock(self, (x, y))
					self.blocks[x, y].add()

		kitten = image.load('q4_map.png')
		self.texture = kitten.get_texture()

	def render(self):
		#glBindTexture(self.texture.target, self.texture.id)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		self.texture.blit(self.pos[0], self.pos[1])

class Block(Entity):
	pass

import types
WHITE = types.SimpleNamespace()
WHITE.r = 1
WHITE.g = 1
WHITE.b = 1

import pyglet
from pyglet.gl import *
from random import random

class SolidBlock(Block):
	def __init__(self, tilemap, pos):
		super().__init__()
		self.tilemap = tilemap
		'''self.body = game.world.CreateBody()
		self.body.type = b2_staticBody
		#self.body.position = pos
		#self.body.SetPosition(pos)
		self.fixture = self.body.CreateFixture(TileMap.boxFixtureDef)
		self.body.position = pos'''
		self.body = game.world.CreateStaticBody(
                    position=pos,
                    fixtures=b2FixtureDef(
                        shape=b2PolygonShape(box=(0.5, 0.5)),
                        density=5.0)
                )

	def render(self):
		pass
