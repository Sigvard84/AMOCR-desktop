import os

def getProcessedFileName(orgName, qualityPercent, colorDepth):

    orgNameSplit = os.path.splitext(orgName)


    newName = orgNameSplit[0]+'_'+colorDepth+'_'+str(qualityPercent)+'ppt'

    return newName

def addFileSize(filename, fileSizes):
    
    filename.replace(".bmp", "")

    pngSize = str(fileSizes["pngSize"])
    gifSize = str(fileSizes["gifSize"])
    zipSize = str(fileSizes["zipSize"])
    binSize = str(fileSizes["binSize"])

    return filename+'_'+pngSize+'_'+gifSize+'_'+zipSize+'_'+binSize+".bmp"

