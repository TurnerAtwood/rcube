from scipy.misc.common import face
DEFAULT_FACE_COLORS = {'f':'green', 'r':'yellow', 'b':'blue', 'l':'white', 't':'red', 'u':'orange'}
FACE_ORDER_LIST = ['f', 'r', 'b', 'l', 't', 'u']

def dispatch(parm={}):
    httpResponse = {}
    if not 'op' in parm:
        httpResponse['status'] = 'error: missing op'
    elif  parm['op'] == 'create':
        parm.pop('op')
        selectedColors = selectColors(parm)
        uniqueColors = set(selectedColors.values())

        if not len(uniqueColors) == len(selectedColors):
            httpResponse['status'] = 'error: non-unique color(s) specified'
        else:
            httpResponse['status'] = 'created'
            httpResponse['cube'] = createCube(selectedColors)
            
    elif parm['op'] == 'check':
        parm.pop('op')
        selectedColors = selectColors(parm)
        uniqueColors = set(selectedColors.values())

        if not len(uniqueColors) == len(selectedColors):
            httpResponse['status'] = 'error: non-unique color(s) specified'
        else:
            cube = parm['cube'].split(",")
            httpResponse = checkCube(selectedColors, cube)
        
        if not httpResponse:
            httpResponse = getCubeConfig(selectedColors, cube)
            
    return httpResponse

#---------- inward facing methods ----------

def createCube(parm):
    cube = []
    for face in FACE_ORDER_LIST:
        cube += [parm[face]]*9
    
    return cube

def selectColors(parm):
    selectedColors = DEFAULT_FACE_COLORS.copy()
    for specifiedFace in parm:
        if specifiedFace in DEFAULT_FACE_COLORS:
            selectedColors[specifiedFace] = parm[specifiedFace]
    return selectedColors

def checkCube(selectedColors, cube):
    resultDict = {}
    if not len(cube) == 54:
        resultDict['status'] = 'error: cube not sized properly'
        return resultDict
    
    if not isCubeColorCountValid(cube):
        resultDict['status'] = 'error: illegal cube'
        return resultDict
    
    if not isCubeCenterValid(selectedColors, cube):
        resultDict['status'] = 'error: illegal cube'
        return resultDict
    
    return resultDict 

def isCubeColorCountValid(cube):
    foundColors = {}
    for pieceColor in cube:
        if pieceColor in foundColors:
            foundColors[pieceColor] += 1
        else:
            foundColors[pieceColor] = 1
    
    if not len(foundColors) == 6:
        return False
    
    for color in foundColors:
        if not foundColors[color] == 9:
            return False
    
    return True 

def isCubeCenterValid(selectedColors, cube):
    centerIndex = 4
    for face in FACE_ORDER_LIST:
        expectedColor = selectedColors[face]
        actualColor = cube[centerIndex]
        if not expectedColor == actualColor:
            return False
        centerIndex += 9
    
    return True

def getCubeConfig(selectedColors, cube):
    resultDict = {}
    faces = getFaces(selectedColors, cube)
    
    if isCubeFull(faces):
        resultDict['status'] = 'full'
    elif isCubeSpots(faces):
        resultDict['status'] = 'spots'        
    elif isCubeCrosses(faces):
        resultDict['status'] = 'crosses'
    else:
        resultDict['status']= 'unknown'
    return resultDict

def isCubeFull(faces):
    for faceKey in faces:
        face = faces[faceKey]
        foundColors = set()
        for color in face:
            foundColors.add(color)
        if not len(foundColors) == 1:
            return False
    return True

def isCubeSpots(faces):
    for faceKey in faces:
        face = faces[faceKey][:]
        middleColor = face.pop(4)
        firstColor = face[0]
        for color in face:
            if not color == firstColor:
                return False
    return True

def isCubeCrosses(faces):
    cornerList = [0,2,6,8]
    crossList = [1,3,4,5,7]
    for faceKey in faces:
        face = faces[faceKey]
        cornerColor = face[0]
        for index in cornerList:
            if not face[index] == cornerColor:
                return False
            
        crossColor = face[1]
        for index in crossList:
            if not face[index] == crossColor:
                return False
    return True

def getFaces(selectedColors, cube):
    faces = {}
    startIndex = 0
    for face in FACE_ORDER_LIST:
        faces[face] = cube[startIndex:startIndex+9]
        startIndex += 9
    return faces