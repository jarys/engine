__author__ = 'Tomas'
import pygame
from math import sqrt

res = "D://res//"


class Player:
    blaze = pygame.image.load(res + "player_blaze.png")
    blaze_x = blaze.get_size()[0]//2
    blaze_y = blaze.get_size()[1]//2
    speed = 2.0
    r = 20

    def __init__(self, name, color, pos):
        self.name = name
        self.rendered_name = None
        self.color = color
        self.pos = [int(pos[0]), int(pos[1])]
        self.real_pos = [pos[0], pos[1]]
        self.path = []
        self.uni = None

    def set_pos(self, x, y):
        self.real_pos[0] = x
        self.real_pos[1] = y
        self.pos[0] = int(x)
        self.pos[1] = int(y)

    def render(self, surface, camx, camy, gui):
        if self in (gui.selected_entity, gui.focused_entity):
            surface.blit(Player.blaze, (self.pos[0] - camx - Player.blaze_x, self.pos[1] - camy - Player.blaze_y))
            if not self.rendered_name:
                self.rendered_name = pygame.font.Font(None, 25).render(self.name, True, self.color)
            surface.blit(self.rendered_name,
                         (self.pos[0] - self.rendered_name.get_rect()[2]//2 - camx,
                          self.pos[1] - self.rendered_name.get_rect()[3] - camy - Player.r - 8))
        pygame.draw.circle(surface, (0, 0, 0), (self.pos[0] - camx, self.pos[1] - camy), Player.r)
        pygame.draw.circle(surface, self.color, (self.pos[0] - camx, self.pos[1] - camy), Player.r - 2)
        if gui.selected_entity == self:
            if len(self.path) > 0:
                path = [(p[0] - camx, p[1] - camy) for p in [self.pos] + self.path]
                if gui.keys["ctrl"]:
                    path.append(pygame.mouse.get_pos())
                pygame.draw.lines(surface, self.color, False, path)
                if gui.keys["ctrl"]:
                    last_point = self.path[-1]
                    pygame.draw.line(surface, self.color, pygame.mouse.get_pos(), (last_point[0] - camx, last_point[1] - camy))

    def point_in(self, mouse, gui):
        return (mouse[0] - self.real_pos[0])**2 + (mouse[1] - self.real_pos[1])**2 <= Player.r**2

    def update(self, gui):
        if len(self.path) > 0:
            target = self.path[0]
            if target[0] == self.real_pos[0]:
                vx = 0
                vy = target[1] - self.real_pos[1]
                print("00")
            else:
                k = (target[1] - self.real_pos[1])/(target[0] - self.real_pos[0])
                vx = Player.speed/sqrt(1 + k*k)
                if target[0] < self.real_pos[0]:
                    vx *= -1
                vy = k*vx
            new_pos = (self.real_pos[0] + vx, self.real_pos[1] + vy)
            if gui.map[new_pos[0]//gui.block, new_pos[1]//gui.block] == 0:
                #self.set_pos(new_pos[0], new_pos[1])
                gui.client.send("move;" + self.uni + ";" + str(new_pos[0]) + ";" + str(new_pos[1]))
                if (target[0] - self.real_pos[0])**2 + (target[1] - self.real_pos[1])**2 <= Player.speed**2:
                    del self.path[0]
            else:
                self.path = []

        if self == gui.selected_entity:
            if gui.keys["mr"]:
                mouse = pygame.mouse.get_pos()
                mouse = mouse[0] + gui.x, mouse[1] + gui.y
                if gui.keys["ctrl"]:
                    self.path.append(mouse)
                else:
                    self.path = [mouse]

    def add(self, gui):
        self.uni = "p" + gui.get_new_uni()
        gui.entities[self.uni] = self