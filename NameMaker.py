import os


def getProcessedFileName(ogName, qualityPercent):

    ogNameSplited = os.path.splitext(ogName)

    newName = ogNameSplited[0]+'__'+str(qualityPercent)+'ppt'

    return newName