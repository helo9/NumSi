from Grid import Grid
from numpy.linalg import solve as linsolve

class Problem(Grid):
	def createProblem(self,boundaries):
		self.boundaries = boundaries
	
	def solve(self):
		self.result = linsolve(self.Amatrix,self.bvector)
	
	def displaysolution(self):
		import matplotlib.pyplot as plt
		x = [self.cells[(xi,eta)].center.x for y in range(self.sizeeta+1) for x in range(self.sizexi+1)]
		y = [self.cells[(xi,eta)].center.y for y in range(self.sizeeta+1) for x in range(self.sizexi+1)]
		z = self.result
		
		plt.contour(x,y,z)
		plt.contourf(x,y,z)
		#plt.colorbar()
		plt.show()
		
		
		



