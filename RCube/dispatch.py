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