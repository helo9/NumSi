class Point(object):
	def __init__(self,x,y):
		'''constructor defining and intitializing object attributes'''
		self.x = x
		self.y = y
		self._edges = [] # "protected"
			
	def addEdge(self,edge):
		'''add Edge containing Point to edges list'''
		if not edge in self._edges:
			self._edges.append(edge)
	
	def removeEdge(self,edge):
		'''remove Edge containing Point from edges list'''
		self._edges.remove(edge)
	
class Edge(object):
	def __init__(self,p1,p2):
		'''constructor'''
		self.point1 = p1
		self.point2 = p2
		self.point1.addEdge(self)
		self.point2.addEdge(self)
	
	def __del__(self):
		'''destructor removes Edge from edges list'''
		self.point1.removeEdge(self)
		self.point2.removeEdge(self)

class Boundary(object):
	pass

class Volume(object):
	pass

class Mesh(object):
	pass
		

		



		
	
