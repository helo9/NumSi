from Problem import Problem
import numpy

class HeatFlow(Problem):
	def materialproperties(self,ident, Data):
		def setMaterial(acell):
			acell.setData(ident,Data)
		map(setMaterial,self.cells.values)
	
	def diskretize(self):
		
		self.array = numpy.zeros((self.sizexi,self.sizeeta))
		
		for i = range(self.sizexi) 						#zählt xi hoch
			for ii = range(self.sizeeta) 				#zählt eta hoch	
				acell = self.cells((xi,eta))
				P  = acell.center
				E  = self.cells((xi +1 , eta   )).center 
				W  = self.cells((xi -1 , eta   )).center
				S  = self.cells((xi    , eta -1)).center
				N  = self.cells((xi    , eta +1)).center
				NE = self.cells((xi +1 , eta +1)).center 
				NW = self.cells((xi -1 , eta +1)).center
				SE = self.cells((xi +1 , eta -1)).center
				SW = self.cells((xi -1 , eta -1)).center
				ne = acell.getne()
				se = acell.getse()
				nw = acell.getnw()
				sw = acell.getsw()	
				k = acell.getData('kappa')
				
				
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
				
				self.array[xi,eta] = self.array[xi,eta)] - De + Ne*NEgammaP /(NEgammaP + NEgammaE + NEgammaNE + NEgammaN) + Se*SEgammaP /(SEgammaP + SEgammaE + SEgammaSE + SEgammaS)
				
				self.array[xi +1,eta] =   
				
				
				
				
