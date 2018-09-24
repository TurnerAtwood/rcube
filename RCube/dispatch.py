
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
    if 'f' in parm :
        cube += [parm['f']]*9
    else:
        cube += ['green']*9
        
    if 'r' in parm:    
        cube += [parm['r']]*9
    else:
        cube += ['yellow']*9

    cube += ['blue']*9 +  ['white']*9 + ['red']*9 + ['orange']*9
    return cube
