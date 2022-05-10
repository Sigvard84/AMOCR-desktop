from tkinter import TRUE
from PIL import Image, ImageChops, ImageEnhance
import math
import FileFunctions as ff
import subprocess as sub
import db
import os
import cv2
import numpy as np
from cv2 import dnn_superres
from matplotlib import pyplot as plt

WINDOWS = False

def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    # return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return Image.fromarray(img)


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    # return cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    return np.asarray(img)


def grabCut(orgimg):
    imgWidth = orgimg.size[0]
    imgHeight = orgimg.size[1]

    img = convert_from_image_to_cv2(orgimg)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


    mask = np.zeros(img.shape[:2],np.uint8)

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    rect = (0,0,imgWidth,imgHeight)

    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]

    return convert_from_cv2_to_image(img)


def thresholdImage(img, is1bit=False):

    if is1bit:
        img = img.convert('L')
    
    cvIm = convert_from_image_to_cv2(img)
    
    threshIm = cv2.adaptiveThreshold(cvIm,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,511,110) #411, 110

    return convert_from_cv2_to_image(threshIm)


def reduceBrightness(img):
    img = img.convert('L')
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(0.95)


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