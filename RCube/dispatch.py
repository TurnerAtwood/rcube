DEFAULT_FACE_COLORS = {'f':'green', 'r':'yellow', 'b':'blue', 'l':'white', 't':'red', 'u':'orange'}
FACE_ORDER_LIST = ['f', 'r', 'b', 'l', 't', 'u']

def dispatch(parm={}):
    httpResponse = {}
    if not 'op' in parm:
        httpResponse['status'] = 'error: missing op'
    elif  parm['op'] == 'create':
        parm.pop('op')
        selectedColors = DEFAULT_FACE_COLORS.copy()
        invalidKeySpecified = False
        for specifiedFace in parm:
            if specifiedFace not in DEFAULT_FACE_COLORS:
                invalidKeySpecified = True
                break
            selectedColors[specifiedFace] = parm[specifiedFace]
        uniqueColors = set(selectedColors.values())
        
        if invalidKeySpecified:
            httpResponse['status'] = 'error: invalid face specified'
        elif not len(uniqueColors) == len(selectedColors):
            httpResponse['status'] = 'error: non-unique color(s) specified'
        else:
            httpResponse['status'] = 'created'
            httpResponse['cube'] = createCube(selectedColors)
    return httpResponse

#---------- inward facing methods ----------

def createCube(parm):
    cube = []
    for face in FACE_ORDER_LIST:
        cube += [parm[face]]*9
    
    return cube