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

    def test900_010_ShouldReturnErrorOnTwoNonUniqueColors(self):
        queryString="op=create&f=purple&r=purple"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
        
    def test900_020_ShouldReturnErrorOnThreeNonUniqueColors(self):
        queryString="op=create&r=purple&b=purple&l=purple"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
    
    def test900_030_ShouldReturnErrorOnNonUniqueDefaultAndSpecifiedColors(self):
        queryString="op=create&f=yellow"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
        

# Acceptance Tests
#
# 200 dispatch -- op=check
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
#
# Sad path analysis
#
#      input:   parm having at least one element with two faces specified as the same color
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#
#      input:   parm having (key,value): (op,check) and (cube,<cube>) where <cube> is not 54 elements     
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:" 
#
#      input:   parm having (key,value): (op,check) and (cube,<cube>) where <cube> has the wrong number of colors    
#      output:  dictionary consisting of an element with a key of "status" and value starting with "error:"
#
        
# Happy Path

    def test210_010ShouldReturnFullStatus(self):
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

# Sad Path

    def test910_010_ShouldReturnErrorOnTwoNonUniqueColors(self):
        queryString="op=check&f=purple&r=purple"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
    
    def test920_010_ShouldReturnErrorOnBadCubeSize(self):
        queryString='op=check&cube=f,f,f,f,f,f,f,f,f,' + \
                                  'r,r,r,r,r,r,r,r,r,'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])

    def test930_010_ShouldReturnErrorOnBadCubeColors(self):
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
        
    def test940_010_ShouldReturnErrorOnWrongCubeColorsSpecified(self):
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
        
    def test950_010_ShouldReturnErrorOnBadCubeCenters(self):
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
        
