from PIL import Image
import math
import FileFunctions as ff

def makeGrayscale(im):
    
    gsIm = im.convert('L')

    return gsIm

def cropImage(im: Image, box):

    cropImage = im.crop(box)

    return cropImage


def saveImageAsBMP(im, fileName, path):
    im.save(path+fileName+'.bmp')


def saveImageAsPNG(im, fileName, path):
    im.save(path+fileName+'.png')

def saveImageAsGIF(im, fileName, path):
    im.save(path+fileName+'.gif')


def reduceQualityOfImage(im, reducePercentage):
    if reducePercentage > 0:
    
        width = im.size[0]
        height = im.size[1]

        #The real percent, in decimal form, to reduce width and height with to get the proper percent reduction
        realPercent = math.sqrt(1 - (reducePercentage / 100))
        # print('reduceQualityOfImage - >Real precentage to reduce: '+str(realPercent))

        newWidth = int(round(width * realPercent))
        newHeight = int(round(height * realPercent))

        newSize = (newWidth, newHeight)
        reducedIm = im.resize(newSize)

        return reducedIm
    else:
        return im


def getFormatSizes(binPath, fileName, im):
    tempPath = ff.getAbsPath("")

    if binPath != None:
        isBin = True
        pureFileName = fileName.replace(".bin", "")
    elif im != None:
        isBin = False
        pureFileName = fileName.replace(".bmp", "")

    filePath = tempPath + pureFileName

    fileSizes = {}
    
    if isBin:
        fileSizes['binSize'] = ff.getFileSize(binPath, fileName)

        zipPath = tempPath + "zip/"
        ff.makeDirectory(zipPath)

        zipPureName = "0"

        ff.copyFile(binPath, fileName, zipPath, zipPureName+".bin")
        ff.zip(zipPath, zipPureName)

        fileSizes['zipSize'] = ff.getFileSize(tempPath, zipPureName+".zip")
        
        ff.removeFile(zipPath, zipPureName+".bin")
        ff.removeDirectory(ff.getAbsPath("")+"zip")
        ff.removeFile(tempPath, zipPureName+".zip")

    else:
        saveImageAsPNG(im, pureFileName, tempPath)
        saveImageAsGIF(im, pureFileName, tempPath)
        fileSizes['pngSize'] = ff.getFileSize(filePath, ".png")
        fileSizes['gifSize'] = ff.getFileSize(filePath, ".gif")

        ff.removeFile(filePath, ".png")
        ff.removeFile(filePath, ".gif")

    return fileSizes