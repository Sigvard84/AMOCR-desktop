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
SQUARE = (130, 300, 270, 370)

# The ammount of pixels that are reduced for each step
PERCENT_TO_REDUCE = 10

# The ammount steps with reduction that are taken
AMMOUNT_OF_STEPS = 9

#-------------------------------------------------------------------------

# Make bitmaps from the bin files and store them in the input folder:
os.system('./Bitmapizer -bitmapize')


# Define input and output directories and create subfolders for each colour depth:
PATH_INPUT = ff.getAbsPath("bmp_images/input_folder/")
PATH_OUTPUT = ff.getAbsPath('../AMOCR-web/web-app/src/presentation-layer/public/meter-images/')

ff.makeDirectory(PATH_INPUT)
ff.makeDirectory(PATH_OUTPUT)

ff.makeDirectory(PATH_OUTPUT+'8bit/')
ff.makeDirectory(PATH_OUTPUT+'4bit/')
ff.makeDirectory(PATH_OUTPUT+'2bit/')
ff.makeDirectory(PATH_OUTPUT+'1bit/')

# Function should be used with the loopTroughDirectory function in FileFunctions
def loopTroughFunction(filePath, fileName, pathOutput):

    for i in range(0,AMMOUNT_OF_STEPS+1):
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
        
        colorDepth = pathOutput[-5]+pathOutput[-4]+pathOutput[-3]+pathOutput[-2]
        newName = nm.getProcessedFileName(fileName, qualityPercent, colorDepth)
        #print('loopTroughFunction -> NEW Filename: '+ newName)

        imf.saveImageAsBMP(reducedIm, newName, newPathOutput)

outputPath8Bit = PATH_OUTPUT+'8bit/'
ff.loopTroughDirectory(PATH_INPUT, outputPath8Bit, loopTroughFunction)

os.system('./Bitmapizer -convert')

print('All done!')