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
#    outputs:
#
#
# Happy Path

    def test100_610_ShouldCreateOneElementCube(self):
        parm = {'op': 'create'}
        expectedResult = ['green']
        actualResult = RCube.createCube(parm)
        self.assertListEqual(expectedResult, actualResult)
    
    