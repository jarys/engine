__author__ = 'Tomas'

import pygame


def get_line(sx, sy, ex, ey):
    path = set()
    try:
        k = (sy - ey)/(sx - ex)
        if sx > ex:
            sx, ex = ex, sx
            sy, ey = ey, sy
        q = sy - k*sx
        for x in range(int(sx + 1), int(ex + 1)):
            path.add((x, int(k*x + q)))

        shift = 0
        if sy > ey:
            sx, ex = ex, sx
            sy, ey = ey, sy
            shift = 1
        k = 1/k
        q = sx - k*sy
        for y in range(int(sy + 1), int(ey + 1)):
            path.add((int(k*y + q), y - shift))
    except ZeroDivisionError:
        pass
    path.add((int(sx), int(sy)))
    path.add((int(ex), int(ey)))
    return path


class Map(dict):
    def __init__(self):
        dict.__init__(self)

    def render(self, surface, camx, camy, gui):
        for pos, block in self.items():
            if block == 1:
                pygame.draw.rect(surface, (0, 40, 60), (pos[0]*gui.block - camx, pos[1]*gui.block - camy, gui.block, gui.block))

    def update(self, gui):
        pass

    def point_in(self, mouse, gui):
        return False