__author__ = 'Tomas'
import pygame


class Server:
    def __init__(self, number, blocks, map):
        self.number = number
        self.blocks = blocks
        self.connect = set()
        for b in self.blocks:
            for c in ((b[0] + 1, b[1] + 1), (b[0] + 1, b[1] - 1), (b[0], b[1] + 1), (b[0] + 1, b[1]),
                      (b[0] - 1, b[1] - 1), (b[0] - 1, b[1] + 1), (b[0], b[1] - 1), (b[0] - 1, b[1])):
                if map[c] == 0:
                    self.connect.add(c)
        for b in self.blocks:
            self.connect.add(b)

    def render(self, surface, camx, camy, gui):
        for b in self.connect:
            pygame.draw.rect(surface, (128, 0, 64) if self in (gui.selected_entity, gui.focused_entity) else (64, 0, 32), (b[0]*gui.block - camx, b[1]*gui.block - camy, gui.block, gui.block))

        for b in self.blocks:
            pygame.draw.rect(surface, (255, 240, 0) if self in (gui.selected_entity, gui.focused_entity) else (255, 150, 0), (b[0]*gui.block - camx, b[1]*gui.block - camy, gui.block, gui.block))


    def point_in(self, mouse, gui):
        for b in self.blocks:
            if (mouse[0] >= b[0]*gui.block) and (mouse[1] >= b[1]*gui.block) and (mouse[0] < b[0]*gui.block + gui.block) and (mouse[1] < b[1]*gui.block + gui.block):
                return True
        return False

    def update(self, gui):
        pass