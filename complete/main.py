'''
Created on 03.12.2014

@author: David
'''
import Grid
from src.NumSi.complete import Geometry
from src.NumSi.complete.Grid import TestBoundary
from src.NumSi.complete.HeatFlow import HeatFlow

testBound = Grid.TestBoundary()



testGrid = HeatFlow.genAlgebraicGrid(testBound)



     

testGrid.diskretize()




testGrid.display()


   
