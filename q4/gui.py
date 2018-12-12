__author__ = 'Tomas'

import pygame
import time
import threading
from player import Player
from server import Server
from map import Map
from client import Client
res = "D://res//"


class GUI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.current_uni = 0
        self.block = 15
        self.tick = 0
        self.entities = dict()
        self.selected_entity = None
        self.focused_entity = None
        self.client = Client(self)

        self.running = False
        self.x = 0
        self.y = 0
        self.screen = None
        self.keys = {"up": False, "down": False, "right": False, "left": False, "ctrl": False, "ml": False, "mr": False}

        map_image = pygame.image.load(res + "floor(-2).bmp")
        self.w, self.h = map_image.get_size()
        self.map = Map()
        self.entities["map"] = self.map

        servers = dict()
        for x in range(self.w):
            for y in range(self.h):
                b = map_image.get_at((x, y))[1]
                if b == 0:
                    self.map[x, y] = 0
                elif b == 40:
                    self.map[x, y] = 1
                elif b == 240:
                    server_id = map_image.get_at((x, y))[2]
                    if server_id not in servers.keys():
                        servers[server_id] = [(x, y)]
                    else:
                        servers[server_id].append((x, y))
                    self.map[x, y] = 2

        for number, blocks in servers.items():
            self.entities[self.get_new_uni()] = Server(number, blocks, self.map)

        Player("Player1", (255, 94, 44), (750, 410)).add(self)
        Player("Player2", (100, 255, 44), (700, 210)).add(self)
        Player("Player3", (50, 255, 100), (810, 450)).add(self)
        Player("Player4", (70, 70, 255), (800, 260)).add(self)

    def run(self):
        self.client.start()
        self.running = True
        pygame.init()
        self.create_window(1000, 700)
        while self.running:
            start = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.create_window(event.w, event.h)
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.keys["left"] = True
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.keys["right"] = True
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.keys["up"] = True
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.keys["down"] = True
                    elif event.key == pygame.K_LCTRL:
                        self.keys["ctrl"] = True
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.keys["left"] = False
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.keys["right"] = False
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.keys["up"] = False
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.keys["down"] = False
                    elif event.key == pygame.K_LCTRL:
                        self.keys["ctrl"] = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.keys["ml"] = True
                        self.selected_entity = self.focused_entity
                    if event.button == 3:
                        self.keys["mr"] = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.keys["ml"] = False
                    if event.button == 3:
                        self.keys["mr"] = False

            if self.keys["right"]:
                self.x += self.block
            if self.keys["left"]:
                self.x -= self.block
            if self.keys["up"]:
                self.y -= self.block
            if self.keys["down"]:
                self.y += self.block

            for e in self.entities.values():
                e.update(self)

            mouse = pygame.mouse.get_pos()
            mouse = mouse[0] + self.x, mouse[1] + self.y

            self.focused_entity = None
            for e in self.entities.values():
                if e.point_in(mouse, self):
                    self.focused_entity = e
                    break
            self.screen.fill((0, 0, 0))

            for e in self.entities.values():
                e.render(self.screen, self.x, self.y, self)

            pygame.display.flip()

            wait = 1/60 - (time.time() - start)
            if wait > 0:
                time.sleep(wait)
            self.tick += 1
            if self.tick%60 == 0:
                print("tick:", self.tick)

        self.client.running = False
        pygame.quit()

    def command(self, command):
        command = command.split(",")
        if command[0] == "set":
            self.map[int(command[1]), int(command[2])] = int(command[3])

    def create_window(self, width, height):
        """Updates the window width and height"""
        pygame.display.set_caption('MAP')
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def get_new_uni(self):
        uni = hex(self.current_uni)[2:]
        self.current_uni += 1
        return uni

if __name__ == "__main__":
    GUI().start()