from ast import Lambda
from PIL import Image
import os, sys, io
import ImgFunctions as imf
import FileFunctions as ff
import NameMaker as nm
import TesseractMachine as tm
import db

#                       Settings for the program
#-------------------------------------------------------------------------

# The square that the program will cut out and use
# The first two numbers represent upper left corner of the square
# The last two numbers represent lower right corner of the square
SQUARE = (349, 273, 539, 302)

# The ammount of pixels that are reduced for each step
PERCENT_TO_REDUCE = 5

# The ammount steps with reduction that are taken
AMMOUNT_OF_STEPS = 1

#-------------------------------------------------------------------------

# Make bitmaps from the bin files and store them in the input folder:
#os.system('./Bitmapizer -bitmapize')


# Define input and output directories and create subfolders for each colour depth:
PATH_INPUT = ff.getAbsPath("bmp_images/input_folder/")
PATH_OUTPUT = ff.getAbsPath('../AMOCR-web/web-app/src/presentation-layer/public/meter-images/')
#PATH_OUTPUT = ff.getAbsPath('')

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

        colorDepth = pathOutput[-5]+pathOutput[-4]+pathOutput[-3]+pathOutput[-2]
        newName = nm.getProcessedFileName(fileName, qualityPercent, colorDepth)

        actualFilePath = newPathOutput+newName+"/"

        ff.makeDirectory(actualFilePath)

        imf.saveImageAsBMP(reducedIm, newName, actualFilePath)

ff.loopTroughDirectory(PATH_INPUT, PATH_8BIT, loopTroughInputDir)

os.system('./Bitmapizer -convert')

def loopTroughOutputDir(path, fileName, _):
    
    #path = path.replace("/", "\\")

    if fileName.endswith(".bin"):
        isBin = True
        pureFileName = fileName.replace(".bin", "")

        imf.getFormatSizes(path, fileName, isBin)

    elif fileName.endswith(".bmp"):
        isBin = False
        pureFileName = fileName.replace(".bmp", "")
        
        imf.getFormatSizes(path, fileName, isBin)

    if len(db.binSizes) and len(db.bmpSizes):

        fileSizes = db.binSizes | db.bmpSizes
        # print(f'fileSizes -> {fileSizes}')

        index = fileName.find("bit_")
        depth = fileName[index-1]

        newName = nm.addFileSize(pureFileName, fileSizes)
        newName += ".png"

        # print(f'New name -> {newName}')

        if depth != "4":
            if depth == "1":
                imageName = fileName.split("_", 1)[0]
                ff.renameFile(db.pathBit4[imageName], db.oldBit4Name[imageName]+".png", db.newBit4Name[imageName])
                ff.removeFile(db.pathBit4[imageName], db.oldBit4Name[imageName]+".bmp")
                ff.removeFile(db.pathBit4[imageName], db.oldBit4Name[imageName]+".bin")


            ff.renameFile(path, pureFileName+".png", newName)
            ff.removeFile(path, pureFileName+".bmp")
            ff.removeFile(path, pureFileName+".bin")
        else:
            imageName = fileName.split("_", 1)[0]
            db.pathBit4[imageName] = path
            db.oldBit4Name[imageName] = pureFileName
            db.newBit4Name[imageName] = newName


        db.binSizes = {}
        db.bmpSizes = {}


def getOcrValues(path, filename, _):

    if filename.endswith('.png'):
        file = ff.getAbsPath(path+filename)
        ocrValue = tm.getImageOCR(file)

        splitFileName = filename.split('_', 2)
        imageName, facit, tail = splitFileName[0], splitFileName[1], splitFileName[2]
        newFilename = imageName + '_' + facit + '_' + ocrValue + '_' + tail
        ff.renameFile(path, filename, newFilename)


ff.loopTroughDirectory(PATH_8BIT, PATH_8BIT, loopTroughOutputDir)
ff.loopTroughDirectory(PATH_4BIT, PATH_4BIT, loopTroughOutputDir)
ff.loopTroughDirectory(PATH_2BIT, PATH_2BIT, loopTroughOutputDir)
ff.loopTroughDirectory(PATH_1BIT, PATH_1BIT, loopTroughOutputDir)

print('\nAll files renamed with filesizes.')

ff.loopTroughDirectory(PATH_8BIT, PATH_8BIT, getOcrValues)
ff.loopTroughDirectory(PATH_4BIT, PATH_4BIT, getOcrValues)
ff.loopTroughDirectory(PATH_2BIT, PATH_2BIT, getOcrValues)
ff.loopTroughDirectory(PATH_1BIT, PATH_1BIT, getOcrValues)


print('\nAll files run through Tesseract and renamed.\nAll done!')