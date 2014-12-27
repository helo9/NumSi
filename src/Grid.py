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


class CartesianBoundary(Boundary):
	def __init__(self,xmax,ymax,M,N):
		self.xmax = xmax
		self.ymax = ymax
		self.iM = M
		self.iN = N
	def M(self):
		return self.iM
	def N(self):
		return self.iN
	def getSouth(self,no):
		return Geometry.Point(no*self.xmax/self.iM,0)
	def getNorth(self,no):
		return Geometry.Point(no*self.xmax/self.iM,self.ymax)
	def getWest(self,no):
		return Geometry.Point(0,no*self.ymax/self.iN)
	def getEast(self,no):
		return Geometry.Point(self.xmax,no*self.ymax/self.iN)

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
		self.center = (pts[0]+pts[1]+pts[2]+pts[3])/4
		self.data = dict()
		
	def setData(self,ident,data):
		self.data[ident] = data
	
	def getData(self,ident):
		return self.data[ident]
	
	def getne(self):
	
		return self.points[2]
		
	def getnw(self):
	
		return self.points[3]
	def getse(self):
	
		return self.points[1]
	def getsw(self):
	
		return self.points[0]
	
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
		
		tgrid.sizexi = M 
		tgrid.sizeeta = N

		
		logicpts = [Geometry.Point(x,y) for y in range(N+1) for x in range(M+1)]
		
		tgrid.points = list(map(transform,logicpts))
		tgrid.cells =  dict()
		
		for xi in range(M):
			for eta in range(N):
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
		
	def display(self):
		import matplotlib.pyplot as plt
		
		xcoords = [Point.x for Point in self.points]
		ycoords = [Point.y for Point in self.points]
		plt.plot(xcoords,ycoords,marker='o',color='r',ls='')
		plt.show()

		
