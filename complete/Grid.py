import Geometry

class Boundary(object):
	def M(self):
		pass
	def N(self):
		pass
	def getSouth(self):
		pass
	def getNorth(self):
		pass
	def getEast(self):
		pass
	def getWest(self):
		pass

class TestBoundary(Boundary):
	def __init__(self):
		self.South = Geometry.Polyline()
		self.South.points.append(Geometry.Point(0,0))
		self.South.points.append(Geometry.Point(1,0))
		self.South.points.append(Geometry.Point(2,0))
		self.South.points.append(Geometry.Point(3,0))
		self.North = Geometry.Polyline()
		self.North.points.append(Geometry.Point(0,3))
		self.North.points.append(Geometry.Point(1,3))
		self.North.points.append(Geometry.Point(2,3))
		self.North.points.append(Geometry.Point(3,3))
		self.East  = Geometry.Polyline()
		self.East.points.append(Geometry.Point(3,0))
		self.East.points.append(Geometry.Point(3,1))
		self.East.points.append(Geometry.Point(3,2))
		self.East.points.append(Geometry.Point(3,3))
		self.West  = Geometry.Polyline()
		self.West.points.append(Geometry.Point(0,0))
		self.West.points.append(Geometry.Point(0,1))
		self.West.points.append(Geometry.Point(0,2))
		self.West.points.append(Geometry.Point(0,3))
		
	def M(self):
		return 3
	def N(self):
		return 3
	def getSouth(self,no):
		return self.South.points[no]
	def getNorth(self,no):
		return self.North.points[no]
	def getEast(self,no):
		return self.East.points[no]
	def getWest(self,no):
		return self.West.points[no]

class Cell(object):
	def __init__(self,pts=[]):
		self.points = pts	

class Grid(object):
	@classmethod
	def genAlgebraicGrid(cls,boundary):

		M = boundary.M()
		N = boundary.N()
		xs = boundary.getSouth
		xn = boundary.getNorth
		xe = boundary.getEast
		xw = boundary.getWest
		
		def transform(pt):
			xi = pt.x
			eta = pt.y
			return  xs(xi)*(1-eta/M)+xn(xi)*(eta/M)+xw(eta)*(1-xi/N)+xe(eta)*xi/N\
					-(xn(N)*eta/M+xs(N)*(1-eta/M))*xi/N\
					-(xn(0)*eta/M+xs(0)*(1-eta/M))*(1-xi/N);
		def ptId(xi,eta):
			return xi+(M+1)*eta
		
		tgrid = cls()
		
		logicpts = [Geometry.Point(x,y) for y in range(N+1) for x in range(M+1)]
		
		tgrid.points = list(map(transform,logicpts))
		tgrid.cells =  dict()
		
		for xi in range(M-1):
			for eta in range(N-1):
				pts = []
				pts.append(tgrid.points[ptId(xi,eta)])
				pts.append(tgrid.points[ptId(xi+1,eta)])
				pts.append(tgrid.points[ptId(xi+1,eta+1)])
				pts.append(tgrid.points[ptId(xi,eta+1)])
				tgrid.cells[(xi,eta)] = Cell(pts)
		return tgrid
	
	@classmethod
	def genEllipticGrid(cls,boundary):
		pass
