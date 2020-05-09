import socket,pickle,threading
from engine.net import protocol

class Client:
    def connect(self, address=("",8888)):
        self.address = address
        try:
            self.sock = socket.socket()
            self.sock.connect(self.address)
        except:
            self.sock.close()
            raise

        self.running = False
        
    def send(self, data):
        protocol.send(self.sock, data)

    def recv(self):
        return protocol.recv(self.sock)

    def handle_data(self, data):
        print("[CLIENT] received", data)

    def loop(self):
        while self.running:
            try:
                self.handle_data(self.recv())
            except OSError:
                pass

    def start(self):
        self.running = True
        threading.Thread(target=self.loop).start()
    
    def close(self):
        protocol.send(self.sock, b"client quit")
        self.running = False
        self.sock.close()
