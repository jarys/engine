import random,sys,pickle
from engine.net import client
from engine.entity import Entity
from engine import game

entities = game.entities
classes = dict()

new_object_listeners = []
def new_object_listener(func):
	new_object_listeners.append(func)
	return func

remove_object_listeners = []
def remove_object_listener(func):
	remove_object_listeners.append(func)
	return func

class SimpleClient(client.Client):
	def handle_data(self, data):
		iid  = data["iid"]
		action = data["action"]
		if   action == "call":
			func = data["func"]
			args = data["args"]
			kwargs = data["kwargs"]
			getattr(remove[iid],func)(*args,from_server=True,**kwargs)
		elif action == "remove":
			for l in remove_object_listeners: l(entities[iid])
			entities[iid].remove()
		elif action == "add":
			if iid in entities:
				return
			clas = data["class"]
			args = data["args"]
			kwargs = data["kwargs"]			
			entities[iid] = classes[clas](*args,iid=iid,from_server=True,**kwargs)
			for l in new_object_listeners: l(entities[iid])

	def send(self, data):
		print("sending", data)
		super().send(pickle.dumps(data))

	def recv(self):
		return pickle.loads(super().recv())

client = SimpleClient() 		


def encode_pointers(data):
	if   type(data) in [int,str,bytes,float,bool,NoneType]:
		return data
	elif type(data) in [tuple,list,set,frozenset]:
		return type(data)([encode_pointers(i) for i in data])
	elif type(data) == dict:
		return {encode_pointers(k):encode_pointers(v) for k,v in data.items()}
	else:
		try:
			return data.iid
		except AttributeError:
			raise ValueError("Unsupported type:" + str(type(data)) + ". No iid.")

def decode_pointers(data):
	if   type(data) == int and data.bit_length() == 47:
		return self.entities[data]
	elif type(data) in [int,str,bytes,float,bool,complex,NoneType]:
		return data
	elif type(data) in [tuple,list,set,frozenset]:
		return type(data)([encode_pointers(i) for i in data])
	elif type(data) == dict:
		return {encode_pointers(k):encode_pointers(v) for k,v in data.items()}
	else:
		return ValueError("Unsupported type:" + str(type(data)))

def get_iid():
	return random.randint(2**46,2**47-1)


#def cache_args(func):
#	def wrapper(self, *args, **kwargs):
#		self.args = args
#		self.kwargs = kwargs
#		func(self,*args,**kwargs)

def online_entity(Cls):
	class OnlineEntity(Cls):
		def __init__(self, *args, from_server=False, iid=None, **kwargs):
			if from_server:
				self.iid = iid
				entities[iid] = self
			else:
				self.iid = get_iid()
				client.send({
					"action": "add",
					"iid": self.iid,
					"class":self.__class__.__name__,
					"args":args,
					"kwargs":kwargs
				})
			Cls.__init__(self,*args,**kwargs)

		def add(self):
			pass # implement hidding later

		def remove(self, from_server=False):
			if from_server:
				del entities[self.iid]
			else:
				client.send({
					"action":"remove",
					"iid":self.iid
				})

	OnlineEntity.__name__ = Cls.__name__
	classes[Cls.__name__] = OnlineEntity
	return OnlineEntity

def online_rule(Cls):
	return Cls

def online(func):
	def wrapper(self, *args, from_server=False, **kwargs):
		if from_server:
			func(self, *args, **kwargs)
		else:
			client.send({
				"action": "call",
				"iid": self.iid,
				"func":func.__name__,
				"args":args,
				"kwargs":kwargs
			})

	wrapper.__name__ = func.__name__
	return wrapper

def trasnmitable(Cls):
	globals()[Cls.__name__] = Cls
	return Cls


