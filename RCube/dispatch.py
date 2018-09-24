
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
    if 'f' in parm :
        cube = ['purple']*9 + ['yellow']*9 + ['blue']*9 +  ['white']*9 + ['red']*9 + ['orange']*9
    else:    
        cube = ['green']*9 + ['yellow']*9 + ['blue']*9 +  ['white']*9 + ['red']*9 + ['orange']*9
    return cube
