import pyglet
from pyglet.window import key
import struct
import threading

from camera import Camera

class Game():
	def __init__(self, net=False, physics=False):
		self.entities = {}
		self.groups = {}
		self.updates = []
		self.renders = []
		self.time = 0

		self.camera = Camera()

		self.window = None
		self.keys = None

		self.net = net
		if self.net:
			from client import Client
			self.client = Client()
		self.net_data = []

		self.physics = physics
		if self.physics:
			from Box2D import b2World
			self.world = b2World(gravity=(0, 0), doSleep=True)

		self.running = False

	def loop(self, dt):
		data_to_handle = self.net_data
		self.net_data = []
		for data in data_to_handle:
			self.handle(data)

		if self.physics:
			#timestep, velocity iter, position iter
			self.world.Step(1/120, 6, 2)
			self.world.ClearForces()

		for entity in self.updates:
			entity.update(dt)

		self.window.clear()

		self.camera.render(self.window.width, self.window.height)
		for entity in self.renders:
			entity.render()

		self.time += dt

	def start(self):
		#samples=4
		config = pyglet.gl.Config(sample_buffers=1, samples=1)
		self.window = pyglet.window.Window(800, 600, config=config, resizable=True)

		self.keys = key.KeyStateHandler()
		self.window.push_handlers(self.keys)

		pyglet.clock.schedule_interval(self.loop, 1/120.0)
		self.running = True
		pyglet.app.run()
		self.running = False

		if self.net:
			self.client.quit()

	def handle(self, data):
		print('CLIENT:', data)
		time, ii = struct.unpack('<dI', data[:12])
		command = decode[data[12:16]]
		if command is 'add':
			entity_class = decode[data[16:20]]
			entity = entity_class.create(time=time, ii=ii, data=data[20:])
			self.entities[ii] = entity
			entity.add()
		elif command is 'edit':
			self.entities[ii].edit(data[16:])
		elif command is 'remove':
			entity = self.entities[ii]
			#entity.remove(data=data[16:])
			entity.remove()
			del self.entities[ii]

	def client_loop(self):
		while self.client.running:
			data = self.client.recv()
			self.net_data.append(data)

	def connect(self, host, port):
		self.client.connect(host, port)
		threading.Thread(target=self.client_loop).start()

game = Game(physics=True)