# -*- coding: iso-8859-15 -*-

from Problem import Problem
import numpy as np

np = np

class TestSourceTerm(object):
	def __init__(self):
		self.SourceTerm = dict()
		self.SourceTerm[(35,35)] = -1


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
			#accepts logical coordinates + direction('n','s','o' and 'w')
			
			if xi ==  0 and direction == 'w':
				print('Adiabater Westrand')
				return [1, 0]
			
			if xi ==  (self.sizexi -1) and direction == 'o':
				print('Ostrand mit dt nach dn = 1')
				return [1, 1]
			
			if eta == 0 and direction == 's':
				print('Suedrand T == 293 K' )
				return[0, 293]
				
			if eta == (self.sizeeta -1) and direction == 'n':
				print('Nordrand T == 273 K')
				return[0,273]
			
			print('no boundary conditon found: something went horribly wrong')	
			return[-1, 0]			 
		
	def diskretize(self):
		# Amatrix describes the heat flow problem, every row contains the conservation equation for one cell
		
		# first row belongs to cell (xi=0,eta=0), second row to cell (xi=0,eta=1) and so on
		self.Amatrix = np.zeros((self.sizexi * self.sizeeta,self.sizexi *self.sizeeta ))      
		self.bvector = np.zeros((self.sizexi * self.sizeeta, 1))    
		
		def getId(axi,aeta):
			return axi*self.sizexi+aeta
		
			
		
		for xi in range(self.sizexi): 					# iteration over xi
			for eta in range(self.sizeeta): 			# iteration over eta
				print('Calculating:(%d/%d,%d/%d)' % (xi,self.sizexi,eta,self.sizeeta))
				acell = self.cells[(xi,eta)]
				P  = acell.center
				ne = acell.getne()
				se = acell.getse()
				sw = acell.getsw()
				nw = acell.getnw()
				sm = (sw + se)/2
				
				try:
					k = acell.getData('kappa')			
				except KeyError:
					print("materialparameter kappa nicht gesetzt setze default")
					k = 1
				
				try:
					q = self.SourceTerm[(xi,eta)]
					print('q = ', q)			
				except KeyError:
					print("quellterm nicht gefunden setze q = 0")
					q  = 0
				
				
				#set source term
				
				self.bvector[getId(xi, eta), 0] += q 
				
				
				#east front
				if xi < self.sizexi-1 :
					# cell is not at east boundary
					E  = self.cells[xi +1 , eta   ].center 
					De = -k*(  (ne.y - se.y)**2 + (ne.x - se.x)**2)/((ne.x - se.x)*(E.y - P.y) - (ne.y - se.y)*(E.x - P.x))
					Ne = -k*(  (ne.y - se.y)*(E.y - P.y) + (ne.x - se.x)*(E.x - P.x))/((ne.y - se.y)*(E.x - P.x) - (ne.x - se.x)*(E.y - P.y))  
					
					#equation 4.15
					self.Amatrix[getId(xi,eta),getId(xi,eta)] -= De
					self.Amatrix[getId(xi,eta),getId(xi+1,eta)] += De
					
					# coefficient eastern cell
					self.Amatrix[getId(xi+1,eta),getId(xi+1,eta)] -= De
					self.Amatrix[getId(xi+1,eta),getId(xi,eta)] += De
					
					if eta == self.sizeeta - 1 :
						print("BErechnung OStfront: KV gehoert zum Nordrand bewechnung einfuegen!")
					
					elif eta == 0 :
						print("Berechnung Ostfront: KV gehoert zum Suedrand berechnung einfuegen!" )
					
					else:
						pass
				
				
				
				
				#Nordfront
				if eta < self.sizeeta-1 :
					#kv geoert nicht zum Nordrand
					N  = self.cells[xi, eta + 1].center 
					Dn = -k*(  (ne.x - nw.x)**2 + (ne.y - nw.y)**2)/(  (ne.y - nw.y)*(N.x - P.x) - (ne.x - nw.x)*(N.y - P.y)) 
				
					#Fuellen des ersten Terms Formel 4.15 für aktuelles KV
					self.Amatrix[getId(xi,eta),getId(xi,eta)] -= Dn
					self.Amatrix[getId(xi,eta),getId(xi,eta+1)] += Dn
					
					#Fuer nördliches KV:
					self.Amatrix[getId(xi,eta+1),getId(xi,eta)] += Dn
					self.Amatrix[getId(xi,eta+1),getId(xi,eta +1)] -=  Dn
					
					if xi == self.sizexi - 1 :
						print("BErechnung Nordfront: KV gehoert zum Nordrand bewechnung einfuegen!")
					
					elif xi == 0 :
						print("Berechnung Nordfront: KV gehoert zum Suedrand berechnung einfuegen!" )
					
					else:
						pass
					
				#southernfront
				
				#southern boundary condition
				print('evaluate southern BC')
				
				if eta == 0:
					result = self.getBounCond(xi, eta, 's')
					if result[0] == 0:
						print('Dirichlet Rand')
						Ds = -k*((se.x - sw.x)**2 + (se.y - sw.y)**2)/((se.x - sw.x)*(P.y - sm.y) - (se.y - sw.y)*(P.x - sm.x))
						self.Amatrix[getId(xi, eta),getId(xi, eta)] += Ds
						self.bvector[getId(xi, eta)] += result[1] * Ds
						
					if result[0] == 1:
						print('Neumann Rand noch nicht implementiert')
						
					
					
				
				
				print(self.Amatrix)
				
				print(self.bvector)
				
					
			''''
						E  = self.cells[xi +1 , eta   ].center 
						NE = self.cells[xi +1 , eta +1].center 
						SE = self.cells[xi +1 , eta -1].center
						
						NEgammaE  = abs(ne -N) + abs(ne -P) + abs(ne -NE) 
						NEgammaN  =              abs(ne -P) + abs(ne -NE) + abs(ne -E)
						NEgammaNE = abs(ne -N) + abs(ne -P)               + abs(ne -E)
						NEgammaP  = abs(ne -N)              + abs(ne -NE) + abs(ne -E)
						
						SEgammaE  = abs(se -S) + abs(se -P) + abs(se -SE) 
						SEgammaS  =              abs(se -P) + abs(se -SE) + abs(se -E)
						SEgammaSE = abs(se -S) + abs(se -P)               + abs(se -E)
						SEgammaP  = abs(se -S)              + abs(se -SE) + abs(se -E)
				
				
				
				
				
				
				
				
				
				
				
				
				
				try:
					E  = self.cells[xi +1 , eta   ].center 
					NE = self.cells[xi +1 , eta +1].center 
					SE = self.cells[xi +1 , eta -1].center
					
				except KeyError:
					print('Ostfront konnte nicht gelesen werden alternative Behandlung der RB einfuegen')
					print(xi , eta)
				
				try:
					N  = self.cells[xi    , eta +1].center
					NW = self.cells[xi -1 , eta +1].center
					NE = self.cells[xi +1 , eta +1].center 
					
				except KeyError:
					print('Nordfront konnte nicht gelesen werden alternative Behandlung der RB einfuegen')
					print(xi , eta)
				
				try:
					S  = self.cells[xi    , eta -1].center
					SE = self.cells[xi +1 , eta -1].center
					SW = self.cells[xi -1 , eta -1].center
				
				except KeyError:
					print('Suedfront konnte nicht gelesn werden alternative Behandlung der RB einfuegen')
					print(xi , eta)
				
				try:
					W  = self.cells[xi -1 , eta   ].center
					NW = self.cells[xi -1 , eta +1].center
					SW = self.cells[xi -1 , eta -1].center
				
				except KeyError:
					print('Westfront konnte nicht gelesn werden alternative Behandlung der RB einfuegen')
					print(xi , eta)
					
					ne = acell.getne()
					se = acell.getse()
					nw = acell.getnw()
					sw = acell.getsw()
				
				try:
					k = acell.getData('kappa')			
				except KeyError:
					print("materialparameter kappa nicht gesetzt setze default")
					k = 123
			
			
				
				NEgammaE  = abs(ne -N) + abs(ne -P) + abs(ne -NE) 
				NEgammaN  =              abs(ne -P) + abs(ne -NE) + abs(ne -E)
				NEgammaNE = abs(ne -N) + abs(ne -P)               + abs(ne -E)
				NEgammaP  = abs(ne -N)              + abs(ne -NE) + abs(ne -E)
				
				SEgammaE  = abs(se -S) + abs(se -P) + abs(se -SE) 
				SEgammaS  =              abs(se -P) + abs(se -SE) + abs(se -E)
				SEgammaSE = abs(se -S) + abs(se -P)               + abs(se -E)
				SEgammaP  = abs(se -S)              + abs(se -SE) + abs(se -E)
				
				NWgammaW  = abs(nw -N) + abs(nw -P) + abs(nw -NW) 
				NWgammaN  =              abs(nw -P) + abs(nw -NW) + abs(nw -W)
				NWgammaNW = abs(nw -N) + abs(nw -P)               + abs(nw -W)
				NWgammaP  = abs(nw -N)              + abs(nw -NW) + abs(nw -W)
				
				SWgammaW  = abs(sw -S) + abs(sw -P) + abs(sw -SW) 
				SWgammaS  =              abs(sw -P) + abs(sw -SW) + abs(sw -W)
				SWgammaWE = abs(sw -S) + abs(sw -P)               + abs(sw -W)
				SWgammaP  = abs(sw -S)              + abs(sw -SW) + abs(sw -W)
				
				
				
				#eastern edge
				
				
				De = -k*(  (ne.y - se.y)**2 + (ne.x - se.x)**2)/((ne.x - se.x)*(E.y - P.y) - (ne.y - se.y)*(E.y - P.y))
				Ne = -k*(  (ne.y - se.y)*(E.y - P.y) + (ne.x - se.x)*(E.x - P.x))/((ne.y - se.y)*(E.x - P.x) - (ne.x - se.x)*(E.y - P.y))  
				
				self.Amatrix[xi,eta] = self.Amatrix[xi,eta] - De + Ne*NEgammaP /(NEgammaP + NEgammaE + NEgammaNE + NEgammaN) + SE*SEgammaP /(SEgammaP + SEgammaE + SEgammaSE + SEgammaS)
				
				#self.array[xi +1,eta] =  
				
				'''
				
				
			
