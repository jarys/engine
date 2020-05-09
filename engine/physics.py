try:
	from Box2D import b2Vec2 as Vec2
except ImportError:
	import math
	import random 

	class Vec2:
		def __init__(self, x, y):
			self.x = x
			self.y = y

		def __add__(self, other):
			return Vec2(self.x + other.x, self.y + other.y)

		def __sub__(self, other):
			return Vec2(self.x - other.x, self.y - other.y)

		def __div__(self, other):
			return Vec2(self.x/other, self.y/other)

		def __mul__(self, other):
			return Vec2(self.x * other, self.y * other)

		def __neg__(self):
			return Vec2(-self.x, -self.y)

		def __radd__(self, other):
			return Vec2(self.x + other, self.y + other)

		def __rdiv__(self, other):
			return Vec2(other/self.x, other/self.y)

		def __rmul__(self, other):
			return Vec2(other * self.x, other * self.y)

		def __rsub__(self, other):
			return Vec2(other - self.x, other - self.y)

		def __repr__(self):
			return self.__str__()

		def __str__(self):
			return "Vec2({0}, {1})".format(self.x, self.y)

		def __getitem__(self, key):
			return (self.x, self.y)[key]

		def __iter__(self):
			yield self.x
			yield self.y

		def data(self):
			return (self.x, self.y)  

		@property
		def length(self):
			return math.sqrt(self.square_length())

		def normalized(self):
			length = self.length()
			if length == 0:
				return Vec2(0, 0)
			return Vec2(self.x/length, self.y/length)

		def square_length(self):
			return (self.x * self.x) + (self.y * self.y)
