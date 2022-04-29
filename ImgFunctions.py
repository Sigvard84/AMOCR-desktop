from PIL import Image
import math
import FileFunctions as ff
import subprocess as sub
import db

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


def getFormatSizes(path, fileName, isBin):
    tempPath = ff.getAbsPath("")

    if isBin:
        pureFileName = fileName.replace(".bin", "")
    else:
        pureFileName = fileName.replace(".bmp", "")

    if isBin:
        zipPath = tempPath + "zip/"
        zipPureName = "0"

        ff.makeDirectory(zipPath)
        ff.copyFile(path, fileName, zipPath, zipPureName+".bin")
        ff.zip(zipPath, zipPureName)

        db.binSizes['binSize'] = ff.getFileSize(path, fileName)
        db.binSizes['zipSize'] = ff.getFileSize(tempPath, zipPureName+".zip")
        
        ff.removeFile(zipPath, zipPureName+".bin")
        ff.removeFile(tempPath, zipPureName+".zip")
        ff.removeDirectory(ff.getAbsPath("")+"zip")

    else:

        index = fileName.find("bit_")
        depth = fileName[index-1]

        match depth:
            case "2":
                path4Bit = path.replace("2bit", "4bit")
                fileName = fileName.replace("2bit", "4bit")

                command = ["magick", path4Bit+fileName, "-depth", depth, path+pureFileName+".png"]
                sub.call(command, shell = True)
                
                db.bmpSizes['pngSize'] = ff.getFileSize(path, pureFileName+".png")

            case"1":
                path4Bit = path.replace("1bit", "4bit")
                fileName = fileName.replace("1bit", "4bit")
                command = ["magick", path4Bit+fileName, "-depth", depth, path+pureFileName+".png"]
                sub.call(command, shell = True)
                
                db.bmpSizes['pngSize'] = ff.getFileSize(path, pureFileName+".png")

            case _:
                command = ["magick", path+fileName, "-depth", depth, path+pureFileName+".png"]
                sub.call(command, shell = True)

                db.bmpSizes['pngSize'] = ff.getFileSize(path, pureFileName+".png")
