from server import Server
import threading
from protocol import *
import struct
from time import time


class Overlord(Server):
    def __init__(self):
        super(Overlord, self).__init__()

        self.base = []
        self.events = {}
        self.last_ii = 1
        self.start_time = time()

    def ii(self):
        self.last_ii += 1
        return struct.pack('<I', self.last_ii)

    def handle(self, data):
        print('OVERLORD:', data)
        data = struct.pack('<d', time() - self.start_time) + data
        command = decode[data[12:16]]
        if command is 'add':
            data = data[:8] + self.ii() + data[12:]
            self.events[data[8:12]] = [data]
        elif command is 'edit':
            self.events[data[8:12]].append(data)
        elif command is 'remove':
            del self.events[data[8:12]]

        self.send_to_all(data)

    def connect_func(self,sock,host,port):
        print('OVERLORD: server sucessfully bind')

    def client_connect_func(self,sock,host,port,address):
        print("client connected")
        for data in self.base:
            self.send(data)
        for thread in self.events.values():
            for data in thread:
                self.send(data)

    def client_disconnect_func(self,sock,host,port,address):
        print("OVERLORD: disconnecting client")

    def quit_func(self,host,port):
        print('OVERLORD: server terminated')


overlord = Overlord()
overlord.connect('localhost', 8888)
threading.Thread(target=overlord.serve_forever).start()
overlord.start_time = time()

'''import time
from random import random

looping = True

def loop():
    while looping:
        event = b' add' +  overlord.ii() + b'food' + struct.pack('fff', random()*800, random()*600, random()*2 + 3)
        overlord.send_to_all(event)
        overlord.events.append(event)
        time.sleep(0.5)

threading.Thread(target=loop).start()'''



