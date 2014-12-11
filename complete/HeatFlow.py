from Problem import Problem
import numpy as np

np = np

class HeatFlow(Problem):
	def _init_(self):
		self.Amatrix = np.zeros((1,1))
		
	def materialproperties(self,ident, Data):
		def setMaterial(acell):
			acell.setData(ident,Data)
		map(setMaterial,self.cells.values)
		
	def diskretize(self):
		# Amatrix describes the heat flow problem, every row contains the conservation equation for one cell
		
		# first row belongs to cell (xi=0,eta=0), second row to cell (xi=1,eta=0) and so on
		self.Amatrix = np.zeros((self.sizexi * self.sizeeta,self.sizexi *self.sizeeta ))          
		
		def getId(axi,aeta):
			return axi*self.sizexi+aeta
		
		for xi in range(self.sizexi): 					# iteration over xi
			for eta in range(self.sizeeta): 			# iteration over eta
				acell = self.cells[(xi,eta)]
				P  = acell.center
				try:
					k = acell.getData('kappa')			
				except KeyError:
					print("materialparameter kappa nicht gesetzt setze default")
					k = 1
				
				#east front
				if xi < self.sizexi-1 :
					# cell is not at east boundary
					E  = self.cells[xi +1 , eta   ].center 
					ne = acell.getne()
					se = acell.getse()
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
				print(xi)
				print(eta)
				print(self.Amatrix)
				
				
				#Nordfront
				if eta < self.sizeeta-1 :
					#kv geoert nicht zum Nordrand
					N  = self.cells[xi, eta + 1].center 
					
					nw = acell.getnw()
					ne = acell.getne()
					
					Dn = -k*(  (ne.x - nw.x)**2 + (ne.y - nw.y)**2)/((ne.x - nw.x)*(N.y - P.y) - (ne.y - nw.y)*(N.x - P.x)) 
				
					#Füllen des ersten Terms Formel 4.15 für aktuelles KV
					self.Amatrix[getId(xi,eta),getId(xi,eta)] -= Dn
					self.Amatrix[getId(xi,eta),getId(xi,eta+1)] += Dn
					
					#Für nördliches KV:
					self.Amatrix[getId(xi,eta+1),getId(xi,eta)] += Dn
					self.Amatrix[getId(xi,eta+1),getId(xi,eta +1)] -=  Dn
					
					if xi == self.sizexi - 1 :
						print("BErechnung Nordfront: KV gehoert zum Nordrand bewechnung einfuegen!")
					
					elif xi == 0 :
						print("Berechnung Nordfront: KV gehoert zum Suedrand berechnung einfuegen!" )
					
					else:
						pass
				print(xi)
				print(eta)
				print(self.Amatrix)
					
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
				
				
			
