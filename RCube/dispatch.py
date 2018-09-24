DEFAULT_FACE_COLORS = {'f':'green', 'r':'yellow', 'b':'blue', 'l':'white', 't':'red', 'u':'orange'}

def dispatch(parm={}):
    httpResponse = {}
    if(not('op' in parm)):
        httpResponse['status'] = 'error: missing op'
    elif(parm['op'] == 'create'):
        httpResponse['status'] = 'created'
        httpResponse['cube'] = createCube(parm)
    return httpResponse

#---------- inward facing methods ----------

def createCube(parm):
    cube = []
    for face in DEFAULT_FACE_COLORS:
        if face in parm:
            cube += [parm[face]]*9
        else:
            cube += [DEFAULT_FACE_COLORS[face]]*9
    
    return cube
