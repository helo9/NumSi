from Grid import Grid
from numpy.linalg import solve as linsolve

class Problem(Grid):
	def createProblem(self,boundaries):
		self.boundaries = boundaries
	
	def solve(self):
		self.result = linsolve(self.A,self.b)


