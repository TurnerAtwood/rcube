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
        httpResponse = checkColors(selectedColors)
        
        # httpResponse will be empty if no errors are found with the cube
        if not httpResponse:
            httpResponse['status'] = 'created'
            httpResponse['cube'] = createCube(selectedColors)
            
    elif parm['op'] == 'check':
        parm.pop('op')
        selectedColors = selectColors(parm)
        httpResponse = checkColors(selectedColors)

        if not 'cube' in parm:
            httpResponse['status'] = 'error: cube must be specified'
        else:
            cube = parm['cube'].split(",")
            httpResponse = checkCube(selectedColors, cube)
        
        # httpResponse will be empty if no errors are found with the cube
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

def checkColors(selectedColors):
    resultDict = {}
    uniqueColors = set(selectedColors.values())

    if '' in uniqueColors:
        resultDict['status'] = 'error: face color is missing'
    elif not len(uniqueColors) == len(selectedColors):
        resultDict['status'] = 'error: non-unique color(s) specified'

    return resultDict

def checkCube(selectedColors, cube):
    resultDict = {}
    if not len(cube) == 54:
        resultDict['status'] = 'error: cube not sized properly'
        return resultDict
    
    if not isCubeColorCountValid(cube):
        resultDict['status'] = 'error: illegal cube (bad color count)'
        return resultDict
    
    if not isCubeCenterValid(selectedColors, cube):
        resultDict['status'] = 'error: illegal cube (bad centers)'
        return resultDict
    
    if not isCubeCornerValid(selectedColors, cube):
        resultDict['status'] = 'error: illegal cube (bad corners)'
        return resultDict
    
    if not isCubeEdgesValid(selectedColors, cube):
        resultDict['status'] = 'error: illegal cube (bad edges)'
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

def isCubeCornerValid(selectedColors, cube):
    cornerIndices = [(0,29,42),(2,9,44),(6,35,45),(8,15,47),(11,18,38),(20,27,36),(17,24,53),(26,33,51)]
    foundEdges = set()
    for indices in cornerIndices:
        colors = [cube[index] for index in indices]
        foundEdges.add(tuple(sorted(colors)))
        valid = isColorsAdjacent(selectedColors, colors[0], colors[1])
        valid = valid and isColorsAdjacent(selectedColors, colors[0], colors[2])
        valid = valid and isColorsAdjacent(selectedColors, colors[1], colors[2])
        if not valid:
            return False
    
    if not len(foundEdges) == 8:
        return False
    
    return True

def isCubeEdgesValid(selectedColors, cube):
    edgeIndices = [(1,43),(3,32),(5,12),(7,46),(19,37),(21,14),(23,30),(25,52),(28,39),(10,41),(34,48),(16,50)]
    foundEdges = set()
    for indices in edgeIndices:
        colors = [cube[index] for index in indices]
        foundEdges.add(tuple(sorted(colors)))
        valid = isColorsAdjacent(selectedColors, colors[0], colors[1])
        if not valid:
            return False
    
    if not len(foundEdges) == 12:
        return False
    
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

def isColorsAdjacent(selectedColors, color1, color2):
    adjacentFaces = [('f','r'),('f','l'),('f','t'),('f','u'),
                     ('b','r'),('b','l'),('b','t'),('b','u'),
                     ('t','r'),('t','l'),('u','r'),('u','l')]
    face1 = getFaceofColor(selectedColors, color1)
    face2 = getFaceofColor(selectedColors, color2)
    if (face1,face2) in adjacentFaces:
        return True
    if (face2,face1) in adjacentFaces:
        return True
    return False
    
def getFaceofColor(selectedColors, color):
    for face in selectedColors:
        if selectedColors[face] == color:
            return face
    return ""
    