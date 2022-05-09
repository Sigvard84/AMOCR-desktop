from tkinter import TRUE
from PIL import Image, ImageEnhance, ImageFilter
import math
import FileFunctions as ff
import subprocess as sub
import db
import os
import cv2
from cv2 import dnn_superres

#Import all enhancement filters from pillow
from PIL.ImageFilter import (
   CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)

WINDOWS = False

def makeGrayscale(im):
    gsIm = im.convert('L')
    return gsIm


def reduceBrightness(im):
    darker = ImageEnhance.Brightness(im)
    darkIm = darker.enhance(0.7)
    return darkIm


def increaseContrast(im, level):
    contrastor = ImageEnhance.Contrast(im)
    contrIm = contrastor.enhance(level)
    return contrIm

def cropImage(im: Image, box):
    cropImage = im.crop(box)
    return cropImage

def getContour(im):
    contourIm = im.filter(CONTOUR)
    return contourIm

def getEdges(im):
    edgeIm = im.filter(FIND_EDGES)
    return edgeIm



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
        
        if depth == "2":
            path4Bit = path.replace("2bit", "4bit")
            fileName = fileName.replace("2bit", "4bit")

            if WINDOWS:
                command = ["magick", path4Bit+fileName, "-depth", depth, path+pureFileName+".png"]
                sub.call(command, shell = True)

            else:
                os.system(f'convert {path4Bit+fileName} -depth {depth} {path+pureFileName}.png')
                
            db.bmpSizes['pngSize'] = ff.getFileSize(path, pureFileName+".png")

        elif depth == "1":
            path4Bit = path.replace("1bit", "4bit")
            fileName = fileName.replace("1bit", "4bit")
            
            if WINDOWS:
            
                command = ["magick", path4Bit+fileName, "-depth", depth, path+pureFileName+".png"]
                sub.call(command, shell = True)

            else:
                os.system(f'convert {path4Bit+fileName} -depth {depth} {path+pureFileName}.png')
                
            db.bmpSizes['pngSize'] = ff.getFileSize(path, pureFileName+".png")

        else:

            if WINDOWS:
                command = ["magick", path+fileName, "-depth", depth, path+pureFileName+".png"]
                sub.call(command, shell = True)

            else:
                os.system(f'convert {path+fileName} -depth {depth} {path+pureFileName}.png')

            db.bmpSizes['pngSize'] = ff.getFileSize(path, pureFileName+".png")
    

def superUpscale(path, filename):

    # Create an SR object
    sr = dnn_superres.DnnSuperResImpl_create()

    # Read image
    image = cv2.imread(path+filename)

    # Read the desired model
    # modelPath = ff.getAbsPath("")+"upscale_lib/EDSR_x4.pb"
    modelPath = ff.getAbsPath("")+"upscale_lib/ESPCN_x4.pb"
    sr.readModel(modelPath)

    # Set the desired model and scale to get correct pre- and post-processing
    sr.setModel("espcn", 4)

    # Upscale the image
    result = sr.upsample(image)

    newFilename = filename.replace(".png", "_superUpscale.png")

    # Save the image
    cv2.imwrite(path+newFilename, result)

    return newFilename