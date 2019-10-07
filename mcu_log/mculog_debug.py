import inspect




def showFaultInfo(error_message):

    previousFrame = inspect.currentframe().f_back\

    ( faultFileName,
      faultLineNumber,
      faultFunctionName,
      faultLines,
      faultIndex) = inspect.getframeinfo(previousFrame)

    print("ERROR: "+error_message)
    print("@function:"+str(faultFunctionName))
    print("@module: "+str(faultFileName))
    print("@ line#"+str(faultLineNumber))
    return



