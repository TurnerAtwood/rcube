'''
Created on Sep 24, 2018

@author: Turner
'''
import unittest
import RCube.dispatch as RCube


class CreateCubeTest(unittest.TestCase):

# Unit Tests
#
# 100 CreateCube
# Desired level of confidence is BVA
# Input-Output Analysis
#    inputs:
#        parm:        dictionary of strings to strings; mandatory; validated
#
#    outputs:  
#        dictionary containing a list representing the 54 squares on an unscrambled cube
#          the colors of the faces may or may not be specified in parm
#
# Happy path analysis
#
#    inputs: 
#    outputs:    ['green', 'green', 'green', 
#                    'green', 'green', 'green', 
#                    'green', 'green', 'green', 
#                    'yellow', 'yellow', 'yellow', 
#                    'yellow', 'yellow', 'yellow', 
#                    'yellow', 'yellow', 'yellow',  
#                    'blue', 'blue', 'blue', 
#                    'blue', 'blue', 'blue', 
#                    'blue', 'blue', 'blue', 
#                    'white', 'white', 'white', 
#                    'white', 'white', 'white', 
#                    'white', 'white', 'white', 
#                    'red', 'red', 'red', 
#                    'red', 'red', 'red', 
#                    'red', 'red', 'red', 
#                    'orange', 'orange', 'orange', 
#                    'orange', 'orange', 'orange', 
#                    'orange', 'orange', 'orange']
#
#
# Happy Path

    def test100_010_ShouldCreateMultipleFaceCube(self):
        parm = {'op': 'create'}
        expectedFaces = ['green', 'yellow','blue', 'white', 'red', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[elementIndex])
                elementIndex += 1
        