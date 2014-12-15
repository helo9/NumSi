from Grid import Grid
from numpy.linalg import solve as linsolve
from numpy import array
import numpy

class Problem(Grid):
	def createProblem(self,boundaries):
		self.boundaries = boundaries
	
	def solve(self):
		self.result = linsolve(self.Amatrix,self.bvector)
	
	def displaysolution(self):
		import matplotlib.pyplot as plt
		x = array([self.cells[(xi,eta)].center.x for eta in range(self.sizeeta) for xi in range(self.sizexi)])
		y = array([self.cells[(xi,eta)].center.y for eta in range(self.sizeeta) for xi in range(self.sizexi)])
		X = x.reshape((self.sizexi,self.sizeeta))
		Y = y.reshape((self.sizexi,self.sizeeta))
		z = self.result.reshape((3,3))
		
		plt.contour(X,Y,z)
		plt.contourf(X,Y,z)
		#plt.colorbar()
		plt.show()
		
		
		



