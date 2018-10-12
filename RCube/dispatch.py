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
            httpResponse['status'] = 'full'
            
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