
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
    cube = ['green']*9 + ['yellow']*9 + ['blue']*9 +  ['white']*9 + ['red']*9 + ['orange']*9
    return cube
