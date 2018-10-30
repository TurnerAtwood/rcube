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

#     def test100_610ShouldRotateFrontFaceOnlyClockwise(self):
#         
#         cube = ['0','1','2','3','f','5','6','7','8',
#                 'r','r','r','r','r','r','r','r','r',
#                 'b','b','b','b','b','b','b','b','b',
#                 'l','l','l','l','l','l','l','l','l',
#                 't','t','t','t','t','t','t','t','t',
#                 'u','u','u','u','u','u','u','u','u',]
#         face = 'f'
#         resultCube = RCube.rotateCube(cube, face)
#         expectedCube = ['6','3','0','7','f','1','8','5','2',
#                 'r','r','r','r','r','r','r','r','r',
#                 'b','b','b','b','b','b','b','b','b',
#                 'l','l','l','l','l','l','l','l','l',
#                 't','t','t','t','t','t','t','t','t',
#                 'u','u','u','u','u','u','u','u','u',]
#         self.assertEquals(expectedCube, resultCube)
# 
#     def test100_620ShouldRotateFrontFaceOnlyAntiClockwise(self):
#         
#         cube = ['0','1','2','3','f','5','6','7','8',
#                 'r','r','r','r','r','r','r','r','r',
#                 'b','b','b','b','b','b','b','b','b',
#                 'l','l','l','l','l','l','l','l','l',
#                 't','t','t','t','t','t','t','t','t',
#                 'u','u','u','u','u','u','u','u','u',]
#         face = 'F'
#         resultCube = RCube.rotateCube(cube, face)
#         expectedCube = ['2','5','8','1','f','7','0','3','6',
#                 'r','r','r','r','r','r','r','r','r',
#                 'b','b','b','b','b','b','b','b','b',
#                 'l','l','l','l','l','l','l','l','l',
#                 't','t','t','t','t','t','t','t','t',
#                 'u','u','u','u','u','u','u','u','u',]
#         self.assertEquals(expectedCube, resultCube)
# 
#     def test100_630ShouldRotateFrontFaceAndTopEdgeClockwise(self):
#         
#         cube = ['0','1','2','3','f','5','6','7','8',
#                 '9','10','11','12','r','14','15','16','17',
#                 '18','19','20','21','b','23','24','25','26',
#                 '27','28','29','30','l', '32','33','34','35',
#                 '36','37','38','39','t','41','42','43','44',
#                 '45','46','47','48','u','50','51','52','53',]
#         face = 'f'
#         resultCube = RCube.rotateCube(cube, face)
#         expectedCube = ['6','3','0','7','f','1','8','5','2',
#                 '42','10','11','43','r','14','44','16','17',
#                 '18','19','20','21','b','23','24','25','26',
#                 '27','28','29','30','l', '32','33','34','35',
#                 '36','37','38','39','t','41','42','43','44',
#                 '45','46','47','48','u','50','51','52','53',]
#         self.assertEquals(expectedCube, resultCube)
        
#     def test100_640ShouldRotateFrontFaceTopEdgeBottomEdgeClockwise(self):
#         
#         cube = ['0','1','2','3','f','5','6','7','8',
#                 '9','10','11','12','r','14','15','16','17',
#                 '18','19','20','21','b','23','24','25','26',
#                 '27','28','29','30','l', '32','33','34','35',
#                 '36','37','38','39','t','41','42','43','44',
#                 '45','46','47','48','u','50','51','52','53',]
#         face = 'f'
#         resultCube = RCube.rotateCube(cube, face)
#         expectedCube = ['6','3','0','7','f','1','8','5','2',
#                 '42','10','11','43','r','14','44','16','17',
#                 '18','19','20','21','b','23','24','25','26',
#                 '27','28','45','30','l', '46','33','34','47',
#                 '36','37','38','39','t','41','42','43','44',
#                 '45','46','47','48','u','50','51','52','53',]
#         self.assertEquals(expectedCube, resultCube)
    
    def test100_650ShouldRotateFrontFaceAllEdgesClockwise(self):
        
        cube = ['0','1','2','3','f','5','6','7','8',
                '9','10','11','12','r','14','15','16','17',
                '18','19','20','21','b','23','24','25','26',
                '27','28','29','30','l', '32','33','34','35',
                '36','37','38','39','t','41','42','43','44',
                '45','46','47','48','u','50','51','52','53',]
        face = 'f'
        resultCube = RCube.rotateCube(cube, face)
        expectedCube = ['6','3','0','7','f','1','8','5','2',
                        '42','10','11','43','r','14','44','16','17',
                        '18','19','20','21','b','23','24','25','26',
                        '27','28','45','30','l', '46','33','34','47',
                        '36','37','38','39','t','41','35','32','29',
                        '15','12','9','48','u','50','51','52','53',]
        self.assertEquals(expectedCube, resultCube)

    def test100_660ShouldRotateBackFace(self):
        
        cube = ['0','1','2','3','f','5','6','7','8',
                '9','10','11','12','r','14','15','16','17',
                '18','19','20','21','b','23','24','25','26',
                '27','28','29','30','l', '32','33','34','35',
                '36','37','38','39','t','41','42','43','44',
                '45','46','47','48','u','50','51','52','53',]
        face = 'b'
        resultCube = RCube.rotateCube(cube, face)
        expectedCube = ['0','1','2','3','f','5','6','7','8',
                        '9','10','53','12','r','52','15','16','51',
                        '24','21','18','25','b','19','26','23','20',
                        '38','28','29','37','l', '32','36','34','35',
                        '11','14','17','39','t','41','42','43','44',
                        '45','46','47','48','u','50','27','30','33',]
        self.assertEquals(expectedCube, resultCube)

    def test100_661ShouldRotateRightFace(self):
        
        cube = ['0','1','2','3','f','5','6','7','8',
                '9','10','11','12','r','14','15','16','17',
                '18','19','20','21','b','23','24','25','26',
                '27','28','29','30','l', '32','33','34','35',
                '36','37','38','39','t','41','42','43','44',
                '45','46','47','48','u','50','51','52','53',]
        face = 'r'
        resultCube = RCube.rotateCube(cube, face)
        expectedCube = ['0','1','47','3','f','50','6','7','53',
                '15','12','9','16','r','10','17','14','11',
                '44','19','20','41','b','23','38','25','26',
                '27','28','29','30','l', '32','33','34','35',
                '36','37','2','39','t','5','42','43','8',
                '45','46','24','48','u','21','51','52','18',]
        self.assertEquals(expectedCube, resultCube)