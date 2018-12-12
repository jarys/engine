__author__ = 'Tomas'
import socket
import threading

HOST, PORT = "localhost", 9999


class Client(threading.Thread):
    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.gui = gui
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

    def run(self):
        self.running = True
        while self.running:
            received = self.sock.recv(1024)
            self.evaluate(received)

        self.sock.close()

    def evaluate(self, command):
        pass

    def send(self, data):
        self.sock.sendall((data + "\n").encode())

if __name__ == "__main__":
    c = Client(None)
    while True:
        c.send(input())