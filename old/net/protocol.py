import pickle
import struct

decode = {
	b' add': 'add',
	b'edit': 'edit',
	b'remv': 'remove',
}

encode = {}
for key, value in decode.items():
	encode[value] = key

def add_pair(key, value):
	decode[key] = value
	encode[value] = key

noii = b'none'

class Packet:
	def __init__(self, data):
		self.data = data

def pickle(data):
	return pickle.dumps(Packet(data))

def unpickle(data):
	return pickle.loads(buf).data

def send(sock, data):
	length = struct.pack('!I', len(data))
	sock.sendall(b'size' + length + data)

def recv(sock):
	try:
		protocol = sock.recv(8)
		if protocol[:4] == b'size':
			length, = struct.unpack('!I', protocol[4:])
			return recvall(sock, length)
		else:
			send(sock, b'Invalid protocol, send packet in form:' +
					   b' size[datalength(4bytes unsigned int)]data')
			return b''
	except ConnectionResetError:
		pass
	except ConnectionAbortedError:
		pass
	except OSError:
		pass

def recvall(sock, count):
	buf = b''
	while count:
		newbuf = sock.recv(count)
		if not newbuf: return None
		buf += newbuf
		count -= len(newbuf)
	return buf
