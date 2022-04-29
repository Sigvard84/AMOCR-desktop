import os

def getProcessedFileName(orgName, qualityPercent, colorDepth):

    orgNameSplit = os.path.splitext(orgName)


    newName = f'{orgNameSplit[0]}_{colorDepth}_{str(qualityPercent)}ppt'

    return newName

def addFileSize(filename, fileSizes):
    
    filename.replace(".bmp", "")

    pngSize = str(fileSizes["pngSize"])
    zipSize = str(fileSizes["zipSize"])
    binSize = str(fileSizes["binSize"])

    return f'{filename}_{binSize}_{zipSize}__{pngSize}'

