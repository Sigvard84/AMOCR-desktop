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


def getFormatSizes(fileName, im):
    path = ff.getAbsPath("")

    pureFileName = fileName.replace(".bmp", "")
    filePath = path + pureFileName


    saveImageAsPNG(im, pureFileName, path)
    saveImageAsGIF(im, pureFileName, path)

    zipPath = path + "zip/"
    ff.makeDirectory(zipPath)
    zipName = "0"
    
    saveImageAsBMP(im, zipName, zipPath)

    ff.zip(zipPath, "0")

    fileSizes = {}
    fileSizes['pngSize'] = ff.getFileSize(filePath, ".png")
    fileSizes['gifSize'] = ff.getFileSize(filePath, ".gif")
    fileSizes['zipSize'] = ff.getFileSize(path, zipName+".zip")

    ff.removeFile(filePath, ".png")
    ff.removeFile(filePath, ".gif")
    ff.removeFile(zipPath, zipName+".bmp")
    ff.removeFile(path, zipName+".zip")
    ff.removeDirectory(ff.getAbsPath("")+"/zip")

    return fileSizes