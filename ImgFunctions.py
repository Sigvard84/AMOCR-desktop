from tkinter import TRUE
from PIL import Image, ImageChops
import math
import FileFunctions as ff
import subprocess as sub
import db as db
import os
import cv2
import numpy as np
from cv2 import dnn_superres
from PIL import Image, ImageEnhance, ImageFilter


#Import all enhancement filters from pillow
from PIL.ImageFilter import (
   CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)

WINDOWS = False

def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    # return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return Image.fromarray(img)


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    # return cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    return np.asarray(img)


def thresholdImage(img, is1bit=False):

    if is1bit:
        img = img.convert('L')
    
    cvIm = convert_from_image_to_cv2(img)
    
    threshIm = cv2.adaptiveThreshold(cvIm,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,411,110) #411, 110

    return convert_from_cv2_to_image(threshIm)

def changeBrightness(im, level):
    brightness = ImageEnhance.Brightness(im)
    adjustedIm = brightness.enhance(level)
    return adjustedIm


def changeContrast(im, level):
    contrastor = ImageEnhance.Contrast(im)
    adjustedIm = contrastor.enhance(level)
    return adjustedIm


def tweakNumber(im, position, brightness, contrast):

    if position == 8:
        return adjust8Position(im, brightness, contrast) 
    
    elif position == 7:
        firstPoints = (0, 0, 425, 90)
        middelPoint = (425, 0, 495, 90)
        lastPoints =  (495, 0, 545, 90)
        return adjustImgNumber(im, brightness, contrast, firstPoints, middelPoint, lastPoints)
    
    elif position == 6:
        firstPoints = (0, 0, 350, 90)
        middelPoint = (350, 0, 425, 90)
        lastPoints =  (425, 0, 545, 90)
        return adjustImgNumber(im, brightness, contrast, firstPoints, middelPoint, lastPoints)


def adjustImgNumber(im, brightness, contrast, firstPoints, middelPoint, lastPoints):

    left = cropImage(im, firstPoints)
    middel = cropImage(im, middelPoint)
    right = cropImage(im, lastPoints)
    
    middel = changeBrightness(middel, brightness)
    middel = changeContrast(middel, contrast)

    #resize, first image
    left_size = left.size
    middle_size = middel.size
    right_size = right.size
    new_image = Image.new('L',(left_size[0]+middle_size[0]+right_size[0], left_size[1]))
    
    new_image.paste(left,(0,0))
    new_image.paste(middel,(left_size[0],0))
    new_image.paste(right,(left_size[0]+middle_size[0],0))

    return new_image
    

def adjust8Position(im, brightness, contrast):
    firstDigitsPoints = (0, 0, 500, 90)
    lastDigitPoints = (500, 0, 545, 90)

    firstDigits = cropImage(im, firstDigitsPoints)
    lastDigit = cropImage(im, lastDigitPoints)
    
    enhLastDigit = changeBrightness(lastDigit, brightness)
    enhLastDigit = changeContrast(enhLastDigit, contrast)

    #resize, first image
    left_size = firstDigits.size
    right_size = enhLastDigit.size
    new_image = Image.new('L',(left_size[0]+right_size[0], left_size[1]))
    
    new_image.paste(firstDigits,(0,0))
    new_image.paste(enhLastDigit,(left_size[0],0))

    return new_image




def makeGrayscale(im):
    gsIm = im.convert('L')
    return gsIm

def cropImage(im: Image, box):
    cropImage = im.crop(box)
    return cropImage


def invertImage(img):
    invImg = ImageChops.invert(img)
    return invImg


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

        # The real percent, in decimal form, to reduce width and height with to get the proper percent reduction
        realPercent = math.sqrt(1 - (reducePercentage / 100))

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
    #modelPath = ff.getAbsPath("")+"upscale_lib/EDSR_x4.pb"
    modelPath = ff.getAbsPath("")+"upscale_lib/FSRCNN_x4.pb"
    sr.readModel(modelPath)

    # Set the desired model and scale to get correct pre- and post-processing
    sr.setModel("fsrcnn", 4)

    # Upscale the image
    result = sr.upsample(image)

    newFilename = filename.replace(".png", "_superUpscale.png")

    # Save the image
    cv2.imwrite(path+newFilename, result)

    return newFilename