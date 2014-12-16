import math

class Point(object):
	def __init__(self,x,y):
		'''constructor defining and intitializing object attributes'''
		self.x = x
		self.y = y
	
	def __add__(self,other):
		'''defining + operator'''
		return Point(self.x+other.x,self.y+other.y)
	
	def __sub__(self,other):
		'''defining - operator'''
		return Point(self.x-other.x,self.y-other.y)
	
	def __mul__(self,other):
		'''defining * operator'''
		if isinstance(other,(int,float)):
			return Point(self.x*other,self.y*other)
		elif isinstance(other,Point):
			return Point(self.x*other.x,self.y*other.y)
	
	def __truediv__(self,other):
		'''defining / operator'''
		if isinstance(other,(int,float)):
			return Point(self.x/other,self.y/other)
		elif isinstance(other,Point):
			return Point(self.x/other.x,self.y/other.y)
	
	def __abs__(self):
		return math.sqrt(self.x**2+self.y**2)
	
	def __str__(self):
		return 'Point(%d,%d)' % (self.x,self.y)
	
class Line(object):
	def __init__(self,p1,p2):
		'''constructor'''
		self.point1 = p1
		self.point2 = p2
	
	def getPoint(self,p):
		return self.point1+(self.point2-self.point1)*p
		
	def midPoint(self):
		return getPoint(self,0.5)
	
	def __abs__(self):
		return abs(self.point2-self.point1)

class Polyline(object):
	def __init__(self):
		self.points = []
	
	def getPoint(self,p):
		targetLength = p*abs(self)
		curLength = 0
		lp = None
		
		for point in self.points:
			if lp != None:
				tempLength = abs(point-lp)
				if curLength+tempLength > targetLength:
						return lp+(point-lp)*(targetLength-curLength)/abs(self)
				
				curLength += tempLength
				
			lp = point
			
	def __abs__(self):
		sum(map(abs,self.points))
