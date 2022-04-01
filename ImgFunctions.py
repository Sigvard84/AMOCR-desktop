from PIL import Image
import math

def makeGrayscale(im):
    
    gsIm = im.convert('L')

    return gsIm

def cropImage(im: Image, box):

    cropImage = im.crop(box)

    return cropImage


def saveImageAsBMP(im, fileName, path):
    im.save(path+fileName+'.bmp')


def reduceQualityOfImage(im, reducePercentage):
    if reducePercentage > 0:
    
        width = im.size[0]
        height = im.size[1]

        # print('reduceQualityOfImage - >OG width: '+str(width))
        # print('reduceQualityOfImage - >OG height: '+str(height))

        # print('reduceQualityOfImage - >Precent to reduce: '+str(reducePercentage))

        #The real percent, in decimal form, to reduce width and height with to get the proper percent reduction
        realPercent = math.sqrt(1 - (reducePercentage / 100))
        # print('reduceQualityOfImage - >Real precentage to reduce: '+str(realPercent))

        # print('reduceQualityOfImage - >FLOAT newWidth: '+str(width * realPercent))
        # print('reduceQualityOfImage - >FLOAT newHeight: '+str(height * realPercent))

        newWidth = int(round(width * realPercent))
        newHeight = int(round(height * realPercent))
        
        # print('reduceQualityOfImage - >NEW width: '+str(newWidth))
        # print('reduceQualityOfImage - >NEW height: '+str(newHeight))

        newSize = (newWidth, newHeight)
        reducedIm = im.resize(newSize)

        return reducedIm
    else:
        return im