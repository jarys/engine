import client, server
import threading

s = server.Server()
s.connect(('', 8888))
s.start()

c = client.Client()
c.connect(('', 8888))