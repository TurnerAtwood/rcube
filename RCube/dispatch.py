from copy import deepcopy
from scipy.misc.common import face

DEFAULT_FACE_COLORS = {'f':'green', 'r':'yellow', 'b':'blue', 'l':'white', 't':'red', 'u':'orange'}
FACE_ORDER_LIST = ['f', 'r', 'b', 'l', 't', 'u']

CORNER_INDICES = [(0,29,42),(2,44,9),(6,45,35),(8,15,47),(11,38,18),(20,36,27),(26,33,51),(17,24,53)]
EDGE_INDICES = [(1,43),(3,32),(5,12),(7,46),(19,37),(21,14),(23,30),(25,52),(28,39),(10,41),(34,48),(16,50)]

# These store all the necessary information to perform rotations on edges
DIRECTION_INDICES = {0:[0,1,2], 1:[2,5,8], 2:[6,7,8], 3:[0,3,6]}
ADJACENT_FACES_DIRECTIONS = {('f','r'):(1,3), ('f','u'):(2,0), ('f','l'):(3,1,), ('f','t'):(0,2), 
                             ('b','r'):(3,1), ('b','u'):(2,2), ('b','l'):(1,3), ('b','t'):(0,0),
                             ('r','t'):(0,1), ('r','u'):(2,1), ('l','t'):(0,3), ('l','u'):(2,3)}
FACE_ROTATE_REVERSAL = {'f':[0,1,0,1], 'b':[1,0,1,0], 'r':[1,1,0,0], 't':[0,0,0,1]}


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
            httpResponse['cube'] = createFullCube(selectedColors)
            
    elif parm['op'] == 'check':
        parm.pop('op')
        selectedColors = selectColors(parm)
        httpResponse = checkColors(selectedColors)

        if not 'cube' in parm:
            httpResponse['status'] = 'error: cube must be specified'
        elif not httpResponse:
            cube = parm['cube'].split(",")
            httpResponse = checkCube(selectedColors, cube)
        
        # httpResponse will be empty if no errors are found with the cube
        if not httpResponse:
            httpResponse = getCubeConfig(selectedColors, cube)
    
    else:
        httpResponse['status'] = 'error: bad op specified' 
        
    return httpResponse

#---------- inward facing methods ----------

#---------- op=create ----------
def createFullCube(selectedColors):
    cube = []
    for face in FACE_ORDER_LIST:
        cube += [selectedColors[face]]*9
    
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

#---------- op=check ----------

def checkCube(selectedColors, cube):
    resultDict = {}
    if not len(cube) == 54:
        resultDict['status'] = 'error: cube not sized properly'
        
    elif not isCubeColorCountValid(cube):
        resultDict['status'] = 'error: illegal cube (bad color count)'
        
    elif not isCubeCenterValid(selectedColors, cube):
        resultDict['status'] = 'error: illegal cube (bad centers)'
        
    elif not isCubeCornerValid(selectedColors, cube):
        resultDict['status'] = 'error: illegal cube (bad corners)'
        
    elif not isCubeEdgesValid(selectedColors, cube):
        resultDict['status'] = 'error: illegal cube (bad edges)'
        
    return resultDict 

def isCubeColorCountValid(cube):
    foundColors = {}
    for pieceColor in cube:
        if not pieceColor in foundColors:
            foundColors[pieceColor] = 0
        foundColors[pieceColor] += 1
    
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
    
    foundCorners = set()
    for indices in CORNER_INDICES:
        colors = [cube[index] for index in indices]
        foundCorners.add(tuple(sorted(colors)))
        
        valid = isColorsAdjacent(selectedColors, colors[0], colors[1])
        valid = valid and isColorsAdjacent(selectedColors, colors[0], colors[2])
        valid = valid and isColorsAdjacent(selectedColors, colors[1], colors[2])
        if not valid:
            return False
    
    if not len(foundCorners) == len(CORNER_INDICES):
        return False
    
    return True

def isCubeEdgesValid(selectedColors, cube):
    
    foundEdges = set()
    for indices in EDGE_INDICES:
        colors = [cube[index] for index in indices]
        foundEdges.add(tuple(sorted(colors)))
        
        valid = isColorsAdjacent(selectedColors, colors[0], colors[1])
        if not valid:
            return False
    
    if not len(foundEdges) == len(EDGE_INDICES):
        return False
    
    return True
        
def getCubeConfig(selectedColors, cube):
    resultDict = {}
    faces = getFaces(cube)
    
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
        for pieceColor in face:
            foundColors.add(pieceColor)
            
        if not len(foundColors) == 1:
            return False
        
    return True

def isCubeSpots(faces):
    for faceKey in faces:
        face = faces[faceKey][:]
        face.pop(4)
        firstColor = face[0]
        
        for pieceColor in face:
            if not pieceColor == firstColor:
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

def getFaces(cube):
    faces = {}
    faceIndex = 0
    for face in FACE_ORDER_LIST:
        faces[face] = cube[faceIndex:faceIndex+9]
        faceIndex += 9
        
    return faces

def isColorsAdjacent(selectedColors, color1, color2):
    nonAdjacentFaces=[('f','b'),('r','l'),('t','u')]
    
    face1 = getFaceofColor(selectedColors, color1)
    face2 = getFaceofColor(selectedColors, color2)
    
    if (face1,face2) in nonAdjacentFaces:
        return False
    
    if (face2,face1) in nonAdjacentFaces:
        return False
    
    return True
    
def getFaceofColor(selectedColors, color):
    for face in selectedColors:
        if selectedColors[face] == color:
            return face
    return ""
    
#---------- op=rotate ----------

def rotateCube(cube, rotation):
    faceKey = rotation.lower()
    if not faceKey == rotation:
        for i in range(3):
            cube = rotateCube(cube, faceKey)
        return cube
    
    # Rotate the colors on the indicated face
    movePairs = {0:2, 1:5, 2:8, 3:1, 4:4, 5:7, 6:0, 7:3, 8:6}
    faces = getFaces(cube)
    oldFace = faces[faceKey]
    newFace= ['']*9
    for oldIndex in movePairs:
        newIndex = movePairs[oldIndex]
        newFace[newIndex] = oldFace[oldIndex]
    faces[faceKey] = newFace
    print 'changed ', faceKey
    # Get the required indices and rotational order of adjacent faces
    edges= {}
    edgeOrder = ['']*4
    for potentialEdge in ADJACENT_FACES_DIRECTIONS:
        if not faceKey in potentialEdge:
            continue
        currentFaceIndex = potentialEdge.index(faceKey)
        otherFaceIndex = (currentFaceIndex+1)%2
        direction = ADJACENT_FACES_DIRECTIONS[potentialEdge][otherFaceIndex]
        edgeKey = potentialEdge[otherFaceIndex]
        
        edges[edgeKey] = DIRECTION_INDICES[direction]
        edgeOrder[ADJACENT_FACES_DIRECTIONS[potentialEdge][currentFaceIndex]] = edgeKey
    
    # Perform rotations
    newFaces = deepcopy(faces)
    rotations = FACE_ROTATE_REVERSAL[faceKey]
    for i in range(4):
        rotatedFromFace = faces[edgeOrder[i]]
        rotatedToFace = newFaces[edgeOrder[(i+1)%4]]
        rotatedFromIndices = edges[edgeOrder[i]]
        rotatedToIndices = edges[edgeOrder[(i+1)%4]]
        
        if rotations[i]:
            rotatedToIndices = rotatedToIndices[::-1]
        
        # Reverse indicated edges for the face bing rotated
        for i in range(3):
            fromIndex = rotatedFromIndices[i]
            toIndex = rotatedToIndices[i]
            rotatedToFace[toIndex] = rotatedFromFace[fromIndex]

    # Reconstruct a cube from faces
    resultCube = []
    for face in FACE_ORDER_LIST:
        resultCube += newFaces[face]
    
    print ''
    for face in FACE_ORDER_LIST:
        print newFaces[face]
    print ''
    return resultCube
    