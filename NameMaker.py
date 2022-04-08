import os

def getProcessedFileName(orgName, qualityPercent, colorDepth):

    orgNameSplit = os.path.splitext(orgName)

    newName = orgNameSplit[0]+'_'+colorDepth+'_'+str(qualityPercent)+'ppt'

    return newName