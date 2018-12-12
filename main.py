import game
from Box2D import b2World
game.init(world=b2World(gravity=(0, 0), doSleep=True))

#import rule_connect
#rule_connect.add()
from camera import Camera
Camera().add()

import camera_control
camera_control.add()

import b2draw
b2draw.init()

'''from firefly import Firefly
import random
for _ in range(100):
	Firefly(random.randint(-40, 40), random.randint(-30, 30)).add()'''

from tilemap import TileMap, SolidBlock
tilemap = TileMap((0, 0), (10, 10))
tilemap.add()

game.start()