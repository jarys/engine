import socket
import protocol

class LiteClient:
	def __init__(self):
		self.running = False

	def connect(self, host, port):
		self.host = host
		self.port = port
		try:
			self.sock = socket.socket()
			self.sock.connect((self.host, self.port))
			self.running = True
		except:
			print('[CLIENT]: Connection failed.')
			self.sock.close()
			raise
		
	def send(self, data):
		protocol.send(self.sock, data)

	def recv(self):
		return protocol.recv(self.sock)
	
	def quit(self):
		protocol.send(self.sock, b"client quit")
		self.sock.close()
		self.running = False

import game

class Client(LiteClient):
	def init(self):
		threading.Thread(target=self.loop).start()

	def loop(self):
		while self.running:
			data = self.recv()
			self.handle(data)

	def handle(self, data):
		print('[CLIENT]:', data)
		time, ii = struct.unpack('<dI', data[:12])
		command = protocol.decode[data[12:16]]
		if command is 'add':
			entity_class = protocol.decode[data[16:20]]
			entity = entity_class.create(time=time, ii=ii, data=data[20:])
			entity.add()
		elif command is 'edit':
			game.entities[ii].edit(data[16:])
		elif command is 'remove':
			entity = game.entities[ii]
			entity.remove()