import struct
import pickle

def send(sock, data):
	#data = pickle.dumps(data)
	length = len(data)
	raw_data =  (b'size' + struct.pack('!I', length) + data)
	sock.sendall(raw_data)

def recv(sock):
	protocol = sock.recv(8)
	if protocol[:4] == b'size':
		length, = struct.unpack('!I', protocol[4:])
		data = recv_all(sock,length)
		#data = pickle.loads(data)
		return data
	else:
		send(sock, b'Invalid protocol, send packet in form:' +
				   b' size[datalength(4bytes unsigned int)][data]')
		raise ValueError("Received packet has wrong format.")


def recv_all(sock, count):
	buf = b''
	while count:
		newbuf = sock.recv(count)
		if not newbuf: return None
		buf += newbuf
		count -= len(newbuf)
	return buf