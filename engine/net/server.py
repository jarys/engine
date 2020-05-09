import socket,select,sys,time,threading,pickle,struct
from engine.net import protocol
	
class Server():
	def __init__(self):
		self.sending_socket = None
		self.running = False

	def connect_func(self,sock,address):
		self.log("sucessfully bound to", address)

	def client_connect_func(self,sock,address):
		self.log("client connected from", address)

	def client_disconnect_func(self,sock,address):
		self.log("disconnecting client from", address)

	def close_func(self):
		self.log("server terminated")
		
	def connect(self, address=("",8888)):
		self.address = address
		try:
			self.unconnected_socket = socket.socket()
			self.unconnected_socket.bind(self.address)
			self.unconnected_socket.listen()
			self.connect_func(self.unconnected_socket, address)
		except:
			self.unconnected_socket.close()
			raise
		self.connected_sockets = []
		self.socket_addresses = {}

	def remove_socket(self, sock):
		self.client_disconnect_func(sock, address)
		try:
			address = self.socket_addresses[sock]
			self.connected_sockets.remove(sock)
			del self.socket_addresses[sock]
		except KeyError:
			pass

	def serve_forever(self):
		while self.running:
			input_ready, output_ready, except_ready = select.select(
				[self.unconnected_socket]+self.connected_sockets,[],[])
			for sock in input_ready:
				if sock == self.unconnected_socket:
					#init socket
					connected_socket, address = sock.accept()
					self.connected_sockets.append(connected_socket)
					self.socket_addresses[connected_socket] = address
					self.client_connect_func(connected_socket, address)
				else:
					try:
						data = protocol.recv(sock)
						address = self.socket_addresses[sock]
					except (ValueError, pickle.UnpicklingError, struct.error):
						self.log("wrong packet format")
					except AttributeError:
						self.log("unknown class in pickle data")
					except (BrokenPipeError,ConnectionResetError):
						self.log("broken pipe")
						self.remove_socket(sock)

					if data:
						if data == b"client quit":
							self.remove_socket(sock)
						else:
							self.sending_socket = sock
							self.handle_data(data)
					
	def handle_data(self, data):
		self.log("received:", data)
		#self.send_data_to_all(data)
		#pass

	def respond(self, data):
		try:
			protocol.send(self.sending_socket, data)
			address = self.socket_addresses[self.sending_socket]
		except:
			self.remove_socket(self.sending_socket)

	def broadcast(self, data):
		for socket in self.connected_sockets:
			try:
				protocol.send(socket, data)
				address = self.socket_addresses[socket]
			except:
				self.remove_socket(socket)

	def close(self):
		for socket in self.connected_sockets:
			socket.close()

		self.unconnected_socket.close()
		self.running = False
		self.close_func()

	def log(self, *args, **kwargs):
		print("[SERVER]", *args, **kwargs)

	def start(self):
		self.running = True
		threading.Thread(target=self.serve_forever).start()

class BroadcastServer(Server):
	def handle_data(self, data):
		self.broadcast(data)

if __name__ == "__main__":
	s = BroadcastServer()
	s.connect(("",8888))
	s.start()

	while True:
		try:
			time.sleep(.5)
		except KeyboardInterrupt:
			break

	s.close()

