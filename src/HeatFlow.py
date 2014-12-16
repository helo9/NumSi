# -*- coding: iso-8859-15 -*-

from Problem import Problem
import numpy as np

np = np

class TestSourceTerm(object):
	def __init__(self):
		self.SourceTerm = dict()
		self.SourceTerm[(5,5)] = 10

class HeatFlow(Problem):
	def __init__(self):
		self.Amatrix = np.zeros((1,1))
		self.SourceTerm = dict()
		self.bvector = np.array([0]) 
		
	def materialproperties(self,ident, Data):
		def setMaterial(acell):
			acell.setData(ident,Data)
		map(setMaterial,self.cells.values)
		
	def setSourceTerm(self,st):
		self.SourceTerm = st.SourceTerm
		
	def editSourceTerm(self):
		print('hier kommt jetzt idealerweise eine eingabe um eintraege im dict zu ueberschreiben')
	
	def getBounCond(self,xi,eta,direction):
			#provisional hard coded Boundary conditions
			#Declaration: returns list of length 2 
			#first item: type of BoundaryCondition(n'th deviation in normal direction): 0 refers to Dirichlet BC; 1 refers to neuman BC			-1: error no bc found
			#second item: value
			#accepts logical coordinates + direction('n','s','e' and 'w')
			
			if xi ==  0 and direction == 'w':
				print('Adiabater Westrand')
				return [0,1000]
			
			if xi ==  (self.sizexi -1) and direction == 'e':
				print('Ostrand mit dt nach dn = 1')
				return [1,0]
			
			if eta == 0 and direction == 's':
				print('Suedrand T == 293 K' )
				return[0,0]
				
			if eta == (self.sizeeta -1) and direction == 'n':
				print('Nordrand T == 273 K')
				return[0,500]
			
			print('no boundary conditon found: something went horribly wrong')	
			return[-1, 0]			 
		
	def diskretize(self):
		# Amatrix describes the heat flow problem, every row contains the conservation equation for one cell
		
		# first row belongs to cell (xi=0,eta=0), second row to cell (xi=0,eta=1) and so on
		self.Amatrix = np.zeros((self.sizexi * self.sizeeta,self.sizexi * self.sizeeta ))      
		self.bvector = np.zeros((self.sizexi * self.sizeeta, 1))    
		
		def getId(axi,aeta):
			return axi*(self.sizeeta)+aeta

		for xi in range(self.sizexi): 					# iteration over xi
			for eta in range(self.sizeeta): 			# iteration over eta
				print('Calculating: (%d,%d),(%d,%d)' % (xi,eta,self.sizexi,self.sizeeta) )
				acell = self.cells[(xi,eta)]
				P  = acell.center
				ne = acell.getne()
				se = acell.getse()
				sw = acell.getsw()
				nw = acell.getnw()
				sm = (sw + se)/2
				nm = (nw + ne)/2
				em = (ne + se)/2
				wm = (nw + sw)/2
				
				# Matrix-Ids
				PId = getId(xi,eta)
				NId = getId(xi,eta+1)
				EId = getId(xi+1,eta)
				WId = getId(xi-1,eta)
				SId = getId(xi,eta-1)
				
				print(str((PId,NId,EId,WId,SId)))
				
				try:
					k = acell.getData('kappa')			
				except KeyError:
					print("materialparameter kappa nicht gesetzt setze default")
					k = 1				
						
				#eastern boundary condition
				
				if xi == self.sizexi -1:
					print('evaluate eastern BC')
					result = self.getBounCond(xi, eta, 'e')
					if result[0] == 0:
						print('Dirichlet Rand')
						Ds = -k*((ne.x-se.x)**2+(ne.y-se.y)**2)/((em.x-P.x)*(ne.y-se.y)-(em.y-P.y)*(ne.x-se.x))
						self.Amatrix[PId,PId] -= Ds
						self.bvector[PId] -= result[1] * Ds
						
					if result[0] == 1:
						print('Neumann Rand noch nicht implementiert')
				
				elif xi < self.sizexi-1 :
					# cell is not at east boundary
					E  = self.cells[xi +1 , eta   ].center 
					De = k*((ne.y-se.y)**2+(ne.x-se.x)**2)/((ne.x-se.x)*(E.y-P.y)-(ne.y-se.y)*(E.x-P.x))
					
					#equation 4.15
					self.Amatrix[PId,PId] -= De
					self.Amatrix[PId,EId] += De
					
					# coefficient eastern cell
					self.Amatrix[EId,EId] -= De
					self.Amatrix[EId,PId] += De
					
				#northern boundary condition
				if eta == self.sizeeta -1:
					print('evaluate northern BC')
					result = self.getBounCond(xi, eta, 'n')
					if result[0] == 0:
						print('Dirichlet Rand')
						Ds = -k*((ne.x-nw.x)**2+(ne.y-nw.y)**2)/((ne.x-nw.x)*(nm.y-P.y)-(ne.y-nw.y)*(nm.x-P.x))
						self.Amatrix[PId,PId] -= Ds
						self.bvector[PId] -= result[1] * Ds
						
					elif result[0] == 1:
						print('Neumann Rand noch nicht implementiert')

				elif eta < self.sizeeta-1 :
					#kv geoert nicht zum Nordrand
					N  = self.cells[xi, eta + 1].center 
					Dn = k*((ne.x-nw.x)**2+(ne.y-nw.y)**2)/((ne.y-nw.y)*(N.x-P.x)-(ne.x-nw.x)*(N.y-P.y)) 
				
					#Fuellen des ersten Terms Formel 4.15 für aktuelles KV
					self.Amatrix[PId,PId] -= Dn
					self.Amatrix[PId,NId] += Dn
					
					#Fuer nördliches KV:
					self.Amatrix[NId,PId] += Dn
					self.Amatrix[NId,NId] -= Dn
					
				#southernfront
	
				if eta == 0:
					print('evaluate southern BC')
					result = self.getBounCond(xi, eta, 's')
					if result[0] == 0:
						print('Dirichlet Rand')
						Ds = k*((se.x-sw.x)**2+(se.y-sw.y)**2)/((se.x-sw.x)*(P.y-sm.y)-(se.y-sw.y)*(P.x-sm.x))
						self.Amatrix[PId,PId] += Ds
						self.bvector[PId] += result[1] * Ds
						
					if result[0] == 1:
						print('Neumann Rand noch nicht implementiert')
	
				#western boundary condition
				
				if xi == 0:
					print('evaluate western BC')
					result = self.getBounCond(xi, eta, 'w')
					if result[0] == 0:
						print('Dirichlet Rand')
						Ds = -k*((nw.x-sw.x)**2+(nw.y-sw.y)**2)/((P.x-wm.x)*(nw.y-sw.y)-(P.y-wm.y)*(nw.x-sw.x))
						self.Amatrix[PId,PId] -= Ds
						self.bvector[PId] -= result[1] * Ds
						
					if result[0] == 1:
						print('Neumann Rand noch nicht implementiert')

				print(self.Amatrix)
				
				print(self.bvector)
		
		# add sources
		for key,q in self.SourceTerm.items():
			print(str(key)+'\n'+str(q))
			self.bvector[getId(key[0],key[1])] += q 
				
