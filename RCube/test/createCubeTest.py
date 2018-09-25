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
#    inputs:     parm = {'op': 'create'}
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
#    inputs:     parm = {'op': 'create', 'f': 'purple'}
#    outputs:    ['purple', 'purple', 'purple', 
#                    'purple', 'purple', 'purple', 
#                    'purple', 'purple', 'purple',
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
#    inputs:
#    outputs:
#
# Sad path analysis
# 
#    inputs:
#    outputs:
#
# Happy Path

    def test100_010_ShouldCreateDefaultCube(self):
        parm = {'f':'green', 'r':'yellow', 'b':'blue', 'l':'white', 't':'red', 'u':'orange'}
        expectedFaces = ['green', 'yellow', 'blue', 'white', 'red', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[elementIndex])
                elementIndex += 1
    
    def test100_020_ShouldCreatePurpleFrontCube(self):
        parm = {'f':'purple', 'r':'yellow', 'b':'blue', 'l':'white', 't':'red', 'u':'orange'}
        expectedFaces = ['purple', 'yellow', 'blue', 'white', 'red', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[elementIndex])
                elementIndex += 1
    
    def test100_030_ShouldCreateBlackFrontCube(self):
        parm = {'f':'black', 'r':'yellow', 'b':'blue', 'l':'white', 't':'red', 'u':'orange'}
        expectedFaces = ['black', 'yellow', 'blue', 'white', 'red', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[elementIndex])
                elementIndex += 1
    
    def test100_040_ShouldCreateBlackRightCube(self):
        parm = {'f':'green', 'r':'black', 'b':'blue', 'l':'white', 't':'red', 'u':'orange'}
        expectedFaces = ['green', 'black', 'blue', 'white', 'red', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[elementIndex])
                elementIndex += 1
    
    def test100_050_ShouldCreatePurpleFrontBlackRightCube(self):
        parm = {'f':'purple', 'r':'black', 'b':'blue', 'l':'white', 't':'red', 'u':'orange'}
        expectedFaces = ['purple', 'black', 'blue', 'white', 'red', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[elementIndex])
                elementIndex += 1
    
    def test100_060_ShouldCreatePurpleFrontBlackRightTealUnderCube(self):
        parm = {'f':'purple', 'r':'black', 'b':'blue', 'l':'white', 't':'red', 'u':'teal'}
        expectedFaces = ['purple', 'black', 'blue', 'white', 'red', 'teal']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[elementIndex])
                elementIndex += 1
    
    def test100_070_ShouldCreateBlueFrontGreenRightPurpleBackCube(self):
        parm = {'f':'blue', 'r':'green', 'b':'purple', 'l':'white', 't':'red', 'u':'orange'}
        expectedFaces = ['blue', 'green', 'purple', 'white', 'red', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[elementIndex])
                elementIndex += 1

