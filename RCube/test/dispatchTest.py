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
# Analysis
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
# Happy path 
#      input:   parm having at least one element with a key of "op"        
#      output:  JSON string containing a key of "status" 
#
# Sad path 
#      input:  
#      output:  
#
# Happy Path

    def test200_010ShouldCreateDefaultCubeStatus(self):
        queryString='op=create'
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status',  resultDict)
        self.assertEquals('created', resultDict['status'][0:7])

# Sad Path


    