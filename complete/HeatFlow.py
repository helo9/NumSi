from Problem import Problem
import numpy as np

np = np

class HeatFlow(Problem):
	def _init_(self):
		self.array = np.zeros((1,1))
		
	def materialproperties(self,ident, Data):
		def setMaterial(acell):
			acell.setData(ident,Data)
		map(setMaterial,self.cells.values)
	
	def diskretize(self):
		
		self.array = np.zeros((self.sizexi,self.sizeeta))
		
		for xi in range(self.sizexi -1): 					         	#zählt xi hoch
			for eta in range(self.sizeeta -1): 				#zählt eta hoch	
				acell = self.cells[(xi,eta)]
				P  = acell.center
				
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
				
				self.array[xi,eta] = self.array[xi,eta] - De + Ne*NEgammaP /(NEgammaP + NEgammaE + NEgammaNE + NEgammaN) + SE*SEgammaP /(SEgammaP + SEgammaE + SEgammaSE + SEgammaS)
				
				self.array[xi +1,eta] =  
				
				
				
				
			