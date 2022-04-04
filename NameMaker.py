import os


def getProcessedFileName(ogName, qualityPercent, colorDepth):

    ogNameSplited = os.path.splitext(ogName)

    newName = ogNameSplited[0]+'_'+colorDepth+'_'+str(qualityPercent)+'ppt'

    return newName