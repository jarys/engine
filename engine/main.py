from engine import game
from engine.net.online import client
game.client = client
#from Box2D import b2World
#game.init(world=b2World(gravity=(0, 0), doSleep=True))

#import rule_connect
#rule_connect.add()
from engine.camera import Camera
Camera().add()

from engine.assets import camera_control
camera_control.add()

#import b2draw
#b2draw.init()

#from engine.assets.firefly import Firefly
import random
for _ in range(100):
    pass #Firefly(random.randint(-40, 40), random.randint(-30, 30)).add()

#from engine.assets.tilemap import TileMap, SolidBlock
#tilemap = TileMap((0, 0), (10, 10))
#tilemap.add()

from engine.entity import Entity
from engine.net.online import online, online_entity
from engine import primitives

@online_entity
class Circle(Entity):
    def __init__(self, pos, r, color):
        self.pos = pos
        self.r = r
        self.color = color

    def render(self):
        primitives.circle(self.pos, self.r, color=self.color)

#Circle((0,0),50,4*(.7,)).add()

from engine.assets import hexgrid
from engine.physics import Vec2
class RuleClick(Entity):
    def init(self):
        @game.window.event
        def on_mouse_press(x, y, button, modifiers):
            pos = game.camera.click_transform(Vec2(x,y))
            gx, gy = hexgrid.grid(*pos, 50)
            x, y = hexgrid.pos(gx, gy, 50)
            Circle((x, y), 50, color=4*(.7,)).add()

RuleClick().add()


game.start()