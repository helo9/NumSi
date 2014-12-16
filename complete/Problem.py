from Grid import Grid
from numpy.linalg import solve as linsolve
from numpy import array

class Problem(Grid):
	def createProblem(self,boundaries):
		self.boundaries = boundaries
	
	def solve(self):
		self.result = linsolve(self.Amatrix,self.bvector)
	
	def displaysolution(self):
		import matplotlib.pyplot as plt
		x = array([self.cells[(xi,eta)].center.x for xi in range(self.sizexi) for eta in range(self.sizeeta)])
		y = array([self.cells[(xi,eta)].center.y for xi in range(self.sizexi) for eta in range(self.sizeeta)])
		X = x.reshape((self.sizexi,self.sizeeta))
		Y = y.reshape((self.sizexi,self.sizeeta))
		z = self.result.reshape((self.sizexi,self.sizeeta))
		print(z)
		plt.contour(X,Y,z)
		plt.contourf(X,Y,z)
		plt.colorbar()
		plt.show()
		
		
		



