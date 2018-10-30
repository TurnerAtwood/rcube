'''
Created on Oct 30, 2018

@author: Turner
'''

import unittest
import RCube.dispatch as RCube


class RotateCubeTest(unittest.TestCase):
    
# Unit Tests
#
# 100 RotateCube
# Desired level of confidence is BVA
# Input-Output Analysis
#    inputs:
#        cube: list of strings representing a cube (Doesn't need to be valid)
#        face: string representing which face to rotate and the direction
#
#    outputs:  
#        a list representing the cube after the indicated rotation
#
# Happy path analysis
#
#    inputs:     cube = ['0','1','2','3','f','5','6','7','8',
#                        'r','r','r','r','r','r','r','r','r',
#                        'b','b','b','b','b','b','b','b','b',
#                        'l','l','l','l','l','l','l','l','l',
#                        't','t','t','t','t','t','t','t','t',
#                        'u','u','u','u','u','u','u','u','u',]
#                face = 'f'

#    outputs:    cube = ['6','3','0','7','f','1','8','5','2',
#                        'r','r','r','r','r','r','r','r','r',
#                        'b','b','b','b','b','b','b','b','b',
#                        'l','l','l','l','l','l','l','l','l',
#                        't','t','t','t','t','t','t','t','t',
#                        'u','u','u','u','u','u','u','u','u',]
#
# Sad path analysis
# 
#    inputs:
#    outputs:
#
# Happy Path

    def test100_010ShouldRotateFaceTopClockwise(self):
        
        cube = ['0','1','2','3','f','5','6','7','8',
                'r','r','r','r','r','r','r','r','r',
                'b','b','b','b','b','b','b','b','b',
                'l','l','l','l','l','l','l','l','l',
                't','t','t','t','t','t','t','t','t',
                'u','u','u','u','u','u','u','u','u',]
        face = 'f'
        resultCube = RCube.rotateCube(cube, face)
        expectedCube = ['6','3','0','7','f','1','8','5','2',
                'r','r','r','r','r','r','r','r','r',
                'b','b','b','b','b','b','b','b','b',
                'l','l','l','l','l','l','l','l','l',
                't','t','t','t','t','t','t','t','t',
                'u','u','u','u','u','u','u','u','u',]
        self.assertEquals(expectedCube, resultCube)

    def test100_020ShouldRotateFaceTopAntiClockwise(self):
        
        cube = ['0','1','2','3','f','5','6','7','8',
                'r','r','r','r','r','r','r','r','r',
                'b','b','b','b','b','b','b','b','b',
                'l','l','l','l','l','l','l','l','l',
                't','t','t','t','t','t','t','t','t',
                'u','u','u','u','u','u','u','u','u',]
        face = 'f'
        resultCube = RCube.rotateCube(cube, face)
        expectedCube = ['6','3','0','7','f','1','8','5','2',
                'r','r','r','r','r','r','r','r','r',
                'b','b','b','b','b','b','b','b','b',
                'l','l','l','l','l','l','l','l','l',
                't','t','t','t','t','t','t','t','t',
                'u','u','u','u','u','u','u','u','u',]
        self.assertEquals(expectedCube, resultCube)
        