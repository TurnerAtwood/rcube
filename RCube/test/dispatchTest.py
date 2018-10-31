import unittest
import httplib
import json

class DispatchTest(unittest.TestCase):
        
    def setUp(self):
        self.key = "status"
        self.errorValue = "error:"
        self.operation ="op"
        self.scramble ="create"

    @classmethod
    def setUpClass(cls):
        cls.ERROR = "error:"
        cls.DEFAULT_SIZE = 3
        cls.MICROSERVICE_PATH = "/rcube?"
        cls.MICROSERVICE_URL="127.0.0.1"
        cls.MICROSERVICE_PORT = 5000
#         cls.MICFROSERVICE_URL="umphrda-rcube.mybluemix.net"
#         cls.MICROSERVICE_PORT = 80
        
    def httpGetAndResponse(self, queryString):
        '''Make HTTP request to URL:PORT for /rcube?querystring; result is a JSON string'''
        try:
            theConnection = httplib.HTTPConnection(self.MICROSERVICE_URL, self.MICROSERVICE_PORT)
            theConnection.request("GET", self.MICROSERVICE_PATH + queryString)
            theStringResponse = theConnection.getresponse().read()
            return theStringResponse 
        except Exception as e:
            theStringResponse = "{'diagnostic': 'error: " + str(e) + "'}"
            return theStringResponse
        
    def string2dict(self, httpResponse):
        '''Convert JSON string to dictionary'''
        result = {}
        try:
            jsonString = httpResponse.replace("'", "\"")
            unicodeDictionary = json.loads(jsonString)
            for element in unicodeDictionary:
                if(isinstance(unicodeDictionary[element],unicode)):
                    result[str(element)] = str(unicodeDictionary[element])
                else:
                    result[str(element)] = unicodeDictionary[element]
        except Exception as e:
            result['diagnostic'] = str(e)
        return result
        
# Acceptance Tests
#
# 100 dispatch - basic functionality
# Desired level of confidence: boundary value analysis
# Analysis 
# inputs:     http:// ...myURL... /httpGetAndResponse?parm
#            parm is a string consisting of key-value pairs
#            At a minimum, parm must contain one key of "op"
#
# outputs:    A JSON string containing, at a minimum, a key of "status"
#
# Happy path 
#      input:   parm having at least one element with a key of "op"        
#      output:  JSON string containing a key of "status" 
#
# Sad path 
#      input:   no string       
#      output:  dictionary consisting of an element with a key of "status" and value of "error: missing op"
#
#      input:   valid parm string with at least one key-value pair, no key of "op"
#      output:  dictionary consisting of an element with a key of "status" and value of "error: missing op"
#
#
#
# Note:  These tests require an active web service
#
#
# Happy path

    def test100_010_ShouldReturnSuccessKey(self):
        queryString="op=create"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
    
# Sad path
    
    def test100_900_ShouldReturnErrorOnEmptyParm(self):
        queryString=""
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
    
    def test100_910_ShouldReturnErrorOnMissingOp(self):
        queryString="f=red"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])

    def test100_920_ShouldReturnErrorOnBadOp(self):
        queryString="op=NOTANOP"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])

# Acceptance Tests
#
# 200 dispatch -- op=create
# Desired level of confidence is BVA
# Input-Output Analysis
#    inputs:   http:// ... myURL ... /rcube?op=create<options>
#                where <options> can be zero or one of the following:
#                  f=<string>    String of length .GT. 0   Optional.   Defaults to "green".  Unvalidated
#                  r=<string>    String of length .GT. 0   Optional.   Defaults to "yellow". Unvalidated
#                  b=<string>    String of length .GT. 0   Optional.   Defaults to "blue".   Unvalidated
#                  l=<string>    String of length .GT. 0   Optional.   Defaults to "white".  Unvalidated
#                  t=<string>    String of length .GT. 0   Optional.   Defaults to "red".    Unvalidated
#                  u=<string>    String of length .GT. 0   Optional.   Defaults to "orange". Unvalidated
# 
#    outputs:   default model cube, which is a JSON string: 
#                 {'status': 'created', 'cube': [
#                    'green', 'green', 'green', 
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
#                    'orange', 'orange', 'orange']}        
# 
# Happy path analysis
#      input:   parm having at least one element with a key of "op"        
#      output:  JSON string containing a key of "status" 
# 
#      input:   parm having at least one element with a key of "op"        
#      output:  JSON string containing a key of "cube" 
#
#      input:   parm having at least one element with (key,value): (op,create)      
#      output:  JSON string containing the default value for the key 'cube' 
#
#      input:   parm having at least one element with (key,value): (op,create), (f,purple), (r,black)     
#      output:  JSON string containing a list representing a cube with a purple front and black right
#
#      input:   parm having at least one element with swapped default colors and (key,value): (op,create)    
#      output:  JSON string containing a list representing a cube with swapped default colors for four faces
#
#      input:   parm having at least one element with similar strings 
#                with different cases and (key,value): (op,create)
#
#      output:  JSON string containing a list representing a cube with swapped default colors for four faces
#
# Sad path analysis
#
#      input:   parm having at least one element with two faces specified as the same color
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#
#      input:   parm having at least one element with three faces specified as the same color
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#
#      input:   parm having at least one element with a specified color conflicting with a different face's default
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#
#      input:   parm having at least one element with an invalid key specified
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#
#      input:   parm specifies an empty face
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#

# Happy Path

    def test200_010ShouldCreateDefaultCubeStatus(self):
        queryString='op=create'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status',  resultDict)
        self.assertEquals('created', resultDict['status'][0:7])

    def test200_020ShouldCreateDefaultCubeKey(self):
        queryString='op=create'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('cube',  resultDict) 
    
    def test200_030_ShouldCreateDefaultCubeValue(self):
        queryString='op=create'
        expectedFaces = ['green', 'yellow','blue', 'white', 'red', 'orange']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualResult = resultDict['cube']
        actualElementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[actualElementIndex])
                actualElementIndex += 1
    
    def test200_040_ShouldCreatePurpleFrontBlackRightCube(self):
        queryString='op=create&f=purple&r=black'
        expectedFaces = ['purple', 'black','blue', 'white', 'red', 'orange']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualResult = resultDict['cube']
        actualElementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[actualElementIndex])
                actualElementIndex += 1
    
    def test200_050_ShouldCreateSwappedDefaultColorsCube(self):
        queryString='op=create&f=orange&r=red&t=yellow&u=green'
        expectedFaces = ['orange', 'red','blue', 'white', 'yellow', 'green']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualResult = resultDict['cube']
        actualElementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[actualElementIndex])
                actualElementIndex += 1
    
    def test200_060_ShouldCreateCaseSensitiveColoredCube(self):
        queryString='op=create&f=Yellow&b=White&l=white&t=WHITE&u=2179'
        expectedFaces = ['Yellow', 'yellow','White', 'white', 'WHITE', '2179']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualResult = resultDict['cube']
        actualElementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[actualElementIndex])
                actualElementIndex += 1
    
    def test200_070_ShouldIgnoreInvalidFaceKeyAndCreatePurpleFrontCube(self):
        queryString="op=create&f=purple&z=purple"
        expectedFaces = ['purple', 'yellow','blue', 'white', 'red', 'orange']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualResult = resultDict['cube']
        actualElementIndex = 0
        for faceColor in expectedFaces:
            for _ in range(9):
                self.assertEqual(faceColor, actualResult[actualElementIndex])
                actualElementIndex += 1

# Sad path

    def test200_910_ShouldReturnErrorOnTwoNonUniqueColors(self):
        queryString="op=create&f=purple&r=purple"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
        
    def test200_920_ShouldReturnErrorOnThreeNonUniqueColors(self):
        queryString="op=create&r=purple&b=purple&l=purple"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
    
    def test200_930_ShouldReturnErrorOnNonUniqueDefaultAndSpecifiedColors(self):
        queryString="op=create&f=yellow"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])

    def test200_940_ShouldReturnErrorOnEmptySpecifiedFace(self):
        queryString="op=create&f=&u=u"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
        

# Acceptance Tests
#
# 300 dispatch -- op=check
# Desired level of confidence is BVA
# Input-Output Analysis
#    inputs:   http:// ... myURL ... /rcube?op=check<options>
#                where <options> can be zero or one of the following:
#                  f=<string>    String of length .GT. 0   Optional.   Defaults to "green".  Unvalidated
#                  r=<string>    String of length .GT. 0   Optional.   Defaults to "yellow". Unvalidated
#                  b=<string>    String of length .GT. 0   Optional.   Defaults to "blue".   Unvalidated
#                  l=<string>    String of length .GT. 0   Optional.   Defaults to "white".  Unvalidated
#                  t=<string>    String of length .GT. 0   Optional.   Defaults to "red".    Unvalidated
#                  u=<string>    String of length .GT. 0   Optional.   Defaults to "orange". Unvalidated
#                  cube=<string> String represents list of length = 54    Required.          Unvalidated
# 
#    outputs:   
#                Dictionary containing the status of the cube
#                   The value of status can be one of: 'full', 'crosses', 'spots', 'unknown'.
#                        -OR-
#                   The value of status will be 'error: xxx', where xxx is an error message. 
# 
# Happy path analysis
#
#      input:   parm having (key,value): (op,check) and (cube,<cube>) where <cube> is default     
#      output:  dictionary consisting of an element with a key of "status" and value of "full"
#
#      input:    parm holds a valid cube with the spot configuration
#      output:   {'status': 'spots'}
#
#      input:    parm holds a valid cube with the crosses configuration
#      output:   {'status': 'crosses'}
#     
#      input:    parm holds a valid cube with the unknown configuration
#      output:   {'status': 'unknown'}
#
# Sad path analysis
#
#      input:   parm having at least one element with two faces specified as the same color
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#
#      input:    parm contains a face with no specified value
#      output:   {'status': 'error: xxx'}
#
#      input:    parm does not specify a cube
#      output:   {'status': 'error: xxx'}
#     
#      input:    parm specifies a cube with length not equal to 54
#      output:   {'status': 'error: xxx'}
#
#      input:   parm specifies a cube with invalid color count  
#      output:   {'status': 'error: xxx'}
#
#      input:   parm specifies a valid cube that does not match the specified colors 
#      output:   {'status': 'error: xxx'}
#
#      input:   parm specifies a cube with invalid centers
#      output:   {'status': 'error: xxx'}
#
#      input:   parm specifies a cubee with impossible edges
#      output:   {'status': 'error: xxx'}
#
#      input:   parm specifies a cubee with impossible corners
#      output:   {'status': 'error: xxx'}
#
#      input:   parm specifies a cubee with duplicate edges
#      output:   {'status': 'error: xxx'}
#
#      input:   parm specifies a cubee with duplicate corners
#      output:   {'status': 'error: xxx'}
        
# Happy Path

    def test300_010ShouldReturnFullStatus(self):
        queryString='op=check&cube=green,green,green,green,green,green,green,green,green,' + \
                                  'yellow,yellow,yellow,yellow,yellow,yellow,yellow,yellow,yellow,' + \
                                  'blue,blue,blue,blue,blue,blue,blue,blue,blue,' + \
                                  'white,white,white,white,white,white,white,white,white,' + \
                                  'red,red,red,red,red,red,red,red,red,' + \
                                  'orange,orange,orange,orange,orange,orange,orange,orange,orange'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status',  resultDict)
        self.assertEquals('full', resultDict['status'])
        
    def test300_020_ShouldReturnSpotsStatus(self):
        queryString='op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=' + \
                                  't,t,t,t,f,t,t,t,t,' + \
                                  'b,b,b,b,r,b,b,b,b,' + \
                                  'u,u,u,u,b,u,u,u,u,' + \
                                  'f,f,f,f,l,f,f,f,f,' + \
                                  'l,l,l,l,t,l,l,l,l,' + \
                                  'r,r,r,r,u,r,r,r,r'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('spots',resultDict['status'])
        
    def test300_030_ShouldReturnCrossesStatus(self):
        queryString='op=check&f=w&r=g&b=y&l=b&t=r&u=o&cube=' + \
                                  'r,w,r,w,w,w,r,w,r,' + \
                                  'w,g,w,g,g,g,w,g,w,' + \
                                  'o,y,o,y,y,y,o,y,o,' + \
                                  'y,b,y,b,b,b,y,b,y,' + \
                                  'g,r,g,r,r,r,g,r,g,' + \
                                  'b,o,b,o,o,o,b,o,b'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('crosses',resultDict['status'])

    def test300_040_ShouldReturnUnknownStatus(self):
        queryString='op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=' + \
                                  'f,t,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,f,t,' + \
                                  'u,u,u,u,u,u,u,u,u'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('unknown',resultDict['status'])
        
# Sad Path

    def test300_910_ShouldReturnErrorOnTwoNonUniqueColors(self):
        queryString="op=check&f=purple&r=purple"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
        
    def test300_912_ShouldReturnErrorOnEmptySpecifiedFace(self):
        queryString='op=check&f=&r=r&b=b&l=l&t=t&u=u&cube=' + \
                                  ',,,,,,,,,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,u,u,u,u,u,u,u,u'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
        
    def test300_915_ShouldReturnErrorOnMissingCube(self):
        queryString="op=check"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
    
    def test300_920_ShouldReturnErrorOnBadCubeSize(self):
        queryString='op=check&cube=f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])

    def test300_930_ShouldReturnErrorOnBadCubeColors(self):
        queryString='op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,u,u,u,u,u,u,u,f'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
        
    def test300_940_ShouldReturnErrorOnWrongCubeColorsSpecified(self):
        queryString='op=check&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,u,u,u,u,u,u,u,u'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
        
    def test300_950_ShouldReturnErrorOnBadCubeCenters(self):
        queryString='op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=' + \
                                  'f,f,f,f,r,f,f,f,f,' + \
                                  'r,r,r,r,f,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,u,u,u,u,u,u,u,u'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])

    def test300_960_ShouldReturnErrorOnBadCubeCorners(self):
        queryString='op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'b,r,r,r,r,r,r,r,r,' + \
                                  'r,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,u,u,u,u,u,u,u,u'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])

    def test300_970_ShouldReturnErrorOnBadCubeEdges(self):
        queryString='op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,u,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,b,u,u,u,u,u,u,u'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])

    def test300_980_ShouldReturnErrorOnDuplicateCubeCorners(self):
        queryString='op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,u,t,t,t,t,t,t,' + \
                                  't,u,u,u,u,u,u,u,u'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
        
    def test300_990_ShouldReturnErrorOnDuplicateCubeEdges(self):
        queryString='op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,u,t,t,t,t,t,t,t,' + \
                                  'u,t,u,u,u,u,u,u,u'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])       

# Acceptance Tests
#
# 400 dispatch -- op=rotate
# Desired level of confidence is BVA
# Input-Output Analysis
#    inputs:   http:// ... myURL ... /rcube?op=rotate<options>
#                where <options> can be zero or one of the following:
#                  f=<string>    String of length .GT. 0   Optional.   Defaults to "green".  Unvalidated
#                  r=<string>    String of length .GT. 0   Optional.   Defaults to "yellow". Unvalidated
#                  b=<string>    String of length .GT. 0   Optional.   Defaults to "blue".   Unvalidated
#                  l=<string>    String of length .GT. 0   Optional.   Defaults to "white".  Unvalidated
#                  t=<string>    String of length .GT. 0   Optional.   Defaults to "red".    Unvalidated
#                  u=<string>    String of length .GT. 0   Optional.   Defaults to "orange". Unvalidated
#                  cube=<string> String represents list of length = 54    Required.          Unvalidated
#                rotate=<string> String of length .GT. 0   Optional.      Required.          Unvalidated
# 
#    outputs:   
#                Dictionary containing the rotated cube
#                   The value of status can be 'rotated'
#                        -OR-
#                   The value of status will be 'error: xxx', where xxx is an error message. 
# 
# Happy path analysis
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'f').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its front face rotated clockwise
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'F').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its front face rotated anti-clockwise
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'r').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its right face rotated clockwise
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'R').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its right face rotated anti-clockwise
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'b').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its front face rotated clockwise
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'B').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its front face rotated anti-clockwise
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'l').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its front face rotated clockwise
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'L').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its front face rotated anti-clockwise
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'t').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its front face rotated clockwise
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'T').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its front face rotated anti-clockwise
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'u').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its front face rotated clockwise
#
#      input:   parm having (key,value): (op,rotate), 
#                    (cube,<cube>) where <cube> is valid, and(face,'U').
#      output:  A dictionary having (status,'rotated') and 
#                    (cube,<cube>) where <cube> has had its front face rotated anti-clockwise
#
# Sad path analysis
#
#      input:   parm having (key,value): (op,rotate) and no cube specified
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#
#      input:   parm having (key,value): (op,rotate) and a bad cube specified
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#
#      input:   parm having (key,value): (op,rotate) and no face specified
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#       
#      input:   parm having (key,value): (op,rotate) and a bad face specified
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#

# Happy Path

    def test400_010_ShouldReturnRotatedFrontClockwise(self):
        queryString='op=rotate&f=f&r=r&b=b&l=l&t=t&u=u&face=f&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,u,u,u,u,u,u,u,u'
                                  
        expectedCube = ['f','f','f','f','f','f','f','f','f',
                        't','r','r','t','r','r','t','r','r',
                        'b','b','b','b','b','b','b','b','b',
                        'l','l','u','l','l','u','l','l','u',
                        't','t','t','t','t','t','l','l','l',
                        'r','r','r','u','u','u','u','u','u']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status',  resultDict)
        self.assertEquals('rotated', resultDict['status'])
        self.assertIn('cube',  resultDict)
        self.assertEquals(expectedCube, resultDict['cube'])
    
    def test400_011_ShouldReturnRotatedFrontAntiClockwise(self):
        queryString='op=rotate&f=f&r=r&b=b&l=l&t=t&u=u&face=F&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,u,u,u,u,u,u,u,u'
                                  
        expectedCube = ['f','f','f','f','f','f','f','f','f',
                        'u','r','r','u','r','r','u','r','r',
                        'b','b','b','b','b','b','b','b','b',
                        'l','l','t','l','l','t','l','l','t',
                        't','t','t','t','t','t','r','r','r',
                        'l','l','l','u','u','u','u','u','u']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status',  resultDict)
        self.assertEquals('rotated', resultDict['status'])
        self.assertIn('cube',  resultDict)
        self.assertEquals(expectedCube, resultDict['cube'])

    def test400_020_ShouldReturnRotatedRightClockwise(self):
        queryString='op=rotate&f=f&r=r&b=b&l=l&t=t&u=u&face=r&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,u,u,u,u,u,u,u,u'
                                  
        expectedCube = ['f','f','u','f','f','u','f','f','u',
                        'r','r','r','r','r','r','r','r','r',
                        't','b','b','t','b','b','t','b','b',
                        'l','l','l','l','l','l','l','l','l',
                        't','t','f','t','t','f','t','t','f',
                        'u','u','b','u','u','b','u','u','b']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        
        self.assertIn('status',  resultDict)
        self.assertEquals('rotated', resultDict['status'])
        self.assertIn('cube',  resultDict)
        self.assertEquals(expectedCube, resultDict['cube'])
        
    def test400_030_ShouldReturnRotatedBackClockwise(self):
        queryString='op=rotate&f=f&r=r&b=b&l=l&t=t&u=u&face=b&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,u,u,u,u,u,u,u,u'
                                  
        expectedCube = ['f','f','f','f','f','f','f','f','f',
                        'r','r','u','r','r','u','r','r','u',
                        'b','b','b','b','b','b','b','b','b',
                        't','l','l','t','l','l','t','l','l',
                        'r','r','r','t','t','t','t','t','t',
                        'u','u','u','u','u','u','l','l','l']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status',  resultDict)
        self.assertEquals('rotated', resultDict['status'])
        self.assertIn('cube',  resultDict)
        self.assertEquals(expectedCube, resultDict['cube'])
        
    def test400_040_ShouldReturnRotatedLeftClockwise(self):
        queryString='op=rotate&f=y&r=r&b=w&l=o&t=g&u=b&face=l&cube=' + \
                                  'b,b,b,r,y,r,b,g,g,' + \
                                  'o,y,b,b,r,g,w,g,r,' + \
                                  'w,b,y,w,w,o,y,r,o,' + \
                                  'g,o,o,w,o,g,w,y,r,' + \
                                  'o,y,r,b,g,r,y,w,w,' + \
                                  'y,y,r,o,b,o,g,w,g'
                                  
        expectedCube = ['o','b','b','b','y','r','y','g','g',
                        'o','y','b','b','r','g','w','g','r',
                        'w','b','g','w','w','o','y','r','y',
                        'w','w','g','y','o','o','r','g','o',
                        'o','y','r','o','g','r','y','w','w',
                        'b','y','r','r','b','o','b','w','g']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status',  resultDict)
        self.assertEquals('rotated', resultDict['status'])
        self.assertIn('cube',  resultDict)
        self.assertEquals(expectedCube, resultDict['cube'])

    def test400_050_ShouldReturnRotatedTopAntiClockwise(self):
        queryString='op=rotate&f=y&r=r&b=w&l=o&t=g&u=b&face=T&cube=' + \
                                  'b,b,b,r,y,r,b,g,g,' + \
                                  'o,y,b,b,r,g,w,g,r,' + \
                                  'w,b,y,w,w,o,y,r,o,' + \
                                  'g,o,o,w,o,g,w,y,r,' + \
                                  'o,y,r,b,g,r,y,w,w,' + \
                                  'y,y,r,o,b,o,g,w,g'
                                  
        expectedCube = ['o','o','g','r','y','r','b','g','g',
                        'b','b','b','b','r','g','w','g','r',
                        'b','y','o','w','w','o','y','r','o',
                        'w','b','y','w','o','g','w','y','r',
                        'r','r','w','y','g','w','o','b','y',
                        'y','y','r','o','b','o','g','w','g']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status',  resultDict)
        self.assertEquals('rotated', resultDict['status'])
        self.assertIn('cube',  resultDict)
        self.assertEquals(expectedCube, resultDict['cube'])
        
    def test400_060_ShouldReturnRotatedUnderAntiClockwise(self):
        queryString='op=rotate&f=y&r=r&b=w&l=o&t=g&u=b&face=U&cube=' + \
                                  'b,b,b,r,y,r,b,g,g,' + \
                                  'o,y,b,b,r,g,w,g,r,' + \
                                  'w,b,y,w,w,o,y,r,o,' + \
                                  'g,o,o,w,o,g,w,y,r,' + \
                                  'o,y,r,b,g,r,y,w,w,' + \
                                  'y,y,r,o,b,o,g,w,g'
                                  
        expectedCube = ['b','b','b','r','y','r','w','g','r',
                        'o','y','b','b','r','g','y','r','o',
                        'w','b','y','w','w','o','w','y','r',
                        'g','o','o','w','o','g','b','g','g',
                        'o','y','r','b','g','r','y','w','w',
                        'r','o','g','y','b','w','y','o','g']
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status',  resultDict)
        self.assertEquals('rotated', resultDict['status'])
        self.assertIn('cube',  resultDict)
        self.assertEquals(expectedCube, resultDict['cube'])
            
# Sad Path

    def test400_910_ShouldReturnErrorOnNoCubeSpecified(self):
        queryString='op=rotate&f=f&r=r&b=b&l=l&t=t&u=u&face=f'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        
        self.assertIn('status',  resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
        
    def test400_920_ShouldReturnErrorOnBadCubeSpecified(self):
        queryString='op=rotate&f=f&r=r&b=b&l=l&t=t&u=u&face=f&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,u,t,t,t,t,t,t,' + \
                                  't,u,u,u,u,u,u,u,u'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        
        self.assertIn('status',  resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])

    def test400_930_ShouldReturnErrorOnNoFaceSpecified(self):
        queryString='op=rotate&f=f&r=r&b=b&l=l&t=t&u=u&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,u,u,u,u,u,u,u,u'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        
        self.assertIn('status',  resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])

    def test400_940_ShouldReturnErrorOnBadFaceSpecified(self):
        queryString='op=rotate&f=f&r=r&b=b&l=l&t=t&u=u&face=o&cube=' + \
                                  'f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,' + \
                                  'b,b,b,b,b,b,b,b,b,' + \
                                  'l,l,l,l,l,l,l,l,l,' + \
                                  't,t,t,t,t,t,t,t,t,' + \
                                  'u,u,u,u,u,u,u,u,u'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        
        self.assertIn('status',  resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
        