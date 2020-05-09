import math
sqrt3 = math.sqrt(3)

def grid(x, y, r):
	gy = (((sqrt3*y - x)/2)//r + ((sqrt3*y + x)/2)//r + 2)//3
	gx = (x//r + 1 - gy%2)//2
	return gx, gy

def pos(gx, gy, r):
	y = sqrt3*gy*r
	x = (2*gx + gy%2)*r
	return x, y 
