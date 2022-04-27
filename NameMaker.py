import os

def getProcessedFileName(orgName, qualityPercent, colorDepth, fileSizes):

    orgNameSplit = os.path.splitext(orgName)

    pngSize = str(fileSizes["pngSize"])
    gifSize = str(fileSizes["gifSize"])
    zipSize = str(fileSizes["zipSize"])

    newName = orgNameSplit[0]+'_'+colorDepth+'_'+str(qualityPercent)+'ppt'+'_'+pngSize+'_'+gifSize+'_'+zipSize

    return newName

def addFileSize(filename, fileSizes):
    
    filename.replace(".bmp", "")

    pngSize = str(fileSizes["pngSize"])
    gifSize = str(fileSizes["gifSize"])
    zipSize = str(fileSizes["zipSize"])

    return filename+'_'+pngSize+'_'+gifSize+'_'+zipSize+".bmp"

