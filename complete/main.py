'''
Created on 03.12.2014

@author: David
'''
import Grid
import Geometry
from Grid import TestBoundary
from HeatFlow import HeatFlow
from HeatFlow import TestSourceTerm

testBound = Grid.CartesianBoundary(3,3,10,14)

testST = TestSourceTerm()


testHF = HeatFlow.genAlgebraicGrid(testBound)

testHF.setSourceTerm(testST)
testHF.editSourceTerm()
testHF.diskretize()
testHF.solve()
#print(testHF.result)

testHF.displaysolution()

#testHF.display()

   
