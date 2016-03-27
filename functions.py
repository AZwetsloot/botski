'''Functions or variables used everywhere go here'''
import settings

def reversebit(str):
    str = str.split(".")[::-1]
    out = ""
    c = 0
    for s in str:
        c += 1
        if (c < len(str)):
            out += s + "."
        else:
            out += s
    return out

def internalDebug(msg):
    printDebugMessages = True
    if printDebugMessages:
        print(msg)
    return

def varexists(variable):
    try:
        eval(variable)
        return True
    except:
        return False
    
