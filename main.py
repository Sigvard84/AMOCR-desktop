from ast import Lambda
from PIL import Image
import os, sys, io
import ImgFunctions as imf
import FileFunctions as ff
import NameMaker as nm

#                       Settings for the program
#-------------------------------------------------------------------------

# The square that the program will cut out and use
# The first two numbers represent upper left corner of the square
# The last two numbers represent lower right corner of the square
SQUARE = (349, 271, 539, 302)

# The ammount of pixels that are reduced for each step
PERCENT_TO_REDUCE = 5

# The ammount steps with reduction that are taken
AMMOUNT_OF_STEPS = 2

#-------------------------------------------------------------------------

# Make bitmaps from the bin files and store them in the input folder:
#os.system('./Bitmapizer -bitmapize')


# Define input and output directories and create subfolders for each colour depth:
PATH_INPUT = ff.getAbsPath("bmp_images/input_folder/")
#PATH_OUTPUT = ff.getAbsPath('../AMOCR-web/web-app/src/presentation-layer/public/meter-images/')
PATH_OUTPUT = ff.getAbsPath('')

ff.makeDirectory(PATH_INPUT)
ff.makeDirectory(PATH_OUTPUT)

PATH_8BIT = PATH_OUTPUT+'8bit/'
PATH_4BIT = PATH_OUTPUT+'4bit/'
PATH_2BIT = PATH_OUTPUT+'2bit/'
PATH_1BIT = PATH_OUTPUT+'1bit/'

ff.makeDirectory(PATH_8BIT)
ff.makeDirectory(PATH_4BIT)
ff.makeDirectory(PATH_2BIT)
ff.makeDirectory(PATH_1BIT)

# Function should be used with the loopTroughDirectory function in FileFunctions
def loopTroughInputDir(filePath, fileName, pathOutput):

    for i in range(0, AMMOUNT_OF_STEPS):
        #print('loopTroughFunction -> Loop: '+str(i))
        #print('loopTroughFunction -> Filename: '+ filePath)

        # the quality of the picture in pixels, 100 is orgininal quality
        qualityPercent = 100 - (i * PERCENT_TO_REDUCE)

        newPathOutput = pathOutput+str(qualityPercent)+'ppt/'

        ff.makeDirectory(newPathOutput)

        im = Image.open(filePath+fileName)

        croppedIm = imf.cropImage(im, SQUARE)
        greyIm = imf.makeGrayscale(croppedIm)
        reducedIm = imf.reduceQualityOfImage(greyIm, i*PERCENT_TO_REDUCE)
        
        fileSizes = imf.getFormatSizes(fileName, reducedIm)

        colorDepth = pathOutput[-5]+pathOutput[-4]+pathOutput[-3]+pathOutput[-2]
        newName = nm.getProcessedFileName(fileName, qualityPercent, colorDepth, fileSizes)
        #print('loopTroughFunction -> NEW Filename: '+ newName)

        imf.saveImageAsBMP(reducedIm, newName, newPathOutput)

ff.loopTroughDirectory(PATH_INPUT, PATH_8BIT, loopTroughInputDir)

#os.system('./Bitmapizer -convert')

def loopTroughOutputDir(filePath, fileName, _):

    im = Image.open(filePath+fileName)
    fileSizes = imf.getFormatSizes(fileName, im)
    im.close()

    pureFileName = fileName.replace(".bmp", "")
    newName = nm.addFileSize(pureFileName, fileSizes)   

    ff.renameFile(filePath, fileName, newName)

ff.loopTroughDirectory(PATH_4BIT, PATH_4BIT, loopTroughOutputDir)
ff.loopTroughDirectory(PATH_2BIT, PATH_2BIT, loopTroughOutputDir)
ff.loopTroughDirectory(PATH_1BIT, PATH_1BIT, loopTroughOutputDir)


print('\nAll done!')