'''
Created on 03.12.2014

@author: David
'''
import Grid
from src.NumSi.complete import Geometry
from src.NumSi.complete.Grid import TestBoundary
from src.NumSi.complete.HeatFlow import HeatFlow
from src.NumSi.complete.HeatFlow import TestSourceTerm

testBound = Grid.TestBoundary()

testST = TestSourceTerm()


testHF = HeatFlow.genAlgebraicGrid(testBound)

testHF.setSourceTerm(testST)
testHF.editSourceTerm()
testHF.diskretize()
testHF.solve()
print(testHF.result)

testHF.display()

   
