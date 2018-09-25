DEFAULT_FACE_COLORS = {'f':'green', 'r':'yellow', 'b':'blue', 'l':'white', 't':'red', 'u':'orange'}
FACE_ORDER_LIST = ['f', 'r', 'b', 'l', 't', 'u']

def dispatch(parm={}):
    httpResponse = {}
    if(not('op' in parm)):
        httpResponse['status'] = 'error: missing op'
    elif(parm['op'] == 'create'):
        parm.pop('op')
        selectedColors = DEFAULT_FACE_COLORS.copy()
        for specifiedColor in parm:
            selectedColors[specifiedColor] = parm[specifiedColor]
        uniqueColors = set(selectedColors.values())
        
        if(not len(uniqueColors) == len(selectedColors)):
            httpResponse['status'] = 'error: non-unique color(s) specified'
        else:
            httpResponse['status'] = 'created'
            httpResponse['cube'] = createCube(parm)
    return httpResponse

#---------- inward facing methods ----------

def createCube(parm):
    cube = []
    for face in FACE_ORDER_LIST:
        if face in parm:
            cube += [parm[face]]*9
        else:
            cube += [DEFAULT_FACE_COLORS[face]]*9
    
    return cube