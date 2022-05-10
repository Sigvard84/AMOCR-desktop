from ast import Lambda
from PIL import Image
import os, sys, io
import ImgFunctions as imf
import FileFunctions as ff
import NameMaker as nm
# import TesseractMachine as tm
import db
import GoogleVision as gv

def testing():
    path = ff.getAbsPath("test.png")
    text = gv.detect_text(path)

    print(f'testing -> text: {text}')

#                       Settings for the program
#-------------------------------------------------------------------------

# The square that the program will cut out and use
# The first two numbers represent upper left corner of the square
# The last two numbers represent lower right corner of the square
SQUARE = (168, 250, 713, 340)

# The ammount of pixels that are reduced for each step
PERCENT_TO_REDUCE = 90

# The ammount steps with reduction that are taken
AMMOUNT_OF_STEPS = 2

#-------------------------------------------------------------------------

# Define input and output directories and create subfolders for each colour depth:
PATH_INPUT = ff.getAbsPath("bmp_images/input_folder/")
PATH_OUTPUT = ff.getAbsPath('../AMOCR-web/web-app/src/presentation-layer/public/meter-images/')

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

#                       Actual program
#-------------------------------------------------------------------------
def runProgram():

    # Make bitmaps from the bin files and store them in the input folder:
    #os.system('./Bitmapizer -bitmapize')

    # Greyscale convertion and cropping
    ff.loopTroughDirectory(PATH_INPUT, PATH_8BIT, loopTroughInputDir)

    # Make different color depth
    os.system('./Bitmapizer -convert')

    # Converting to different formats and take sizese
    ff.loopTroughDirectory(PATH_8BIT, PATH_8BIT, loopTroughOutputDir)
    ff.loopTroughDirectory(PATH_4BIT, PATH_4BIT, loopTroughOutputDir)
    ff.loopTroughDirectory(PATH_2BIT, PATH_2BIT, loopTroughOutputDir)
    ff.loopTroughDirectory(PATH_1BIT, PATH_1BIT, loopTroughOutputDir)

    print('\nAll files renamed with filesizes.')

    # Clean up images for better OCR
    ff.loopTroughDirectory(PATH_8BIT, PATH_8BIT, cleanUpImage)
    ff.loopTroughDirectory(PATH_4BIT, PATH_4BIT, cleanUpImage)
    ff.loopTroughDirectory(PATH_2BIT, PATH_2BIT, cleanUpImage)
    ff.loopTroughDirectory(PATH_1BIT, PATH_1BIT, cleanUpImage)

    print('\nAll files cleaned for the OCR.')

    # Make the ocr reading
    ff.loopTroughDirectory(PATH_8BIT, PATH_8BIT, getOcrValues)
    ff.loopTroughDirectory(PATH_4BIT, PATH_4BIT, getOcrValues)
    ff.loopTroughDirectory(PATH_2BIT, PATH_2BIT, getOcrValues)
    ff.loopTroughDirectory(PATH_1BIT, PATH_1BIT, getOcrValues)

    print('\nAll files run through Tesseract and renamed.')

    # Make the superUpscaling and ocr reading on the upscaled image
    ff.loopTroughDirectory(PATH_8BIT, PATH_8BIT, upscale)
    ff.loopTroughDirectory(PATH_4BIT, PATH_4BIT, upscale)
    ff.loopTroughDirectory(PATH_2BIT, PATH_2BIT, upscale)
    ff.loopTroughDirectory(PATH_1BIT, PATH_1BIT, upscale)

    print('\nAll files upscaled and read with OCR!')

    print('\nAll done!')
#-------------------------------------------------------------------------

# Testing
def test():

    PATH_TEST = ff.getAbsPath('bmp_images/testing/')
    PATH_INPUT_TEST = ff.getAbsPath('bmp_images/testing/input/')
    PATH_OUTPUT_TEST = ff.getAbsPath('bmp_images/testing/output/')

    ff.makeDirectory(PATH_TEST)
    ff.makeDirectory(PATH_INPUT_TEST)
    ff.makeDirectory(PATH_OUTPUT_TEST)

    PATH_8BIT_TEST = PATH_OUTPUT_TEST+'8bit/'
    PATH_4BIT_TEST = PATH_OUTPUT_TEST+'4bit/'
    PATH_2BIT_TEST = PATH_OUTPUT_TEST+'2bit/'
    PATH_1BIT_TEST = PATH_OUTPUT_TEST+'1bit/'

    ff.makeDirectory(PATH_8BIT_TEST)
    ff.makeDirectory(PATH_4BIT_TEST)
    ff.makeDirectory(PATH_2BIT_TEST)
    ff.makeDirectory(PATH_1BIT_TEST)

    # # Greyscale convertion and cropping
    # ff.loopTroughDirectory(PATH_INPUT_TEST, PATH_8BIT_TEST, loopTroughInputDir)

    # # Make different color depth
    # os.system('./Bitmapizer -convert')

    # Converting to different formats and take sizese
    ff.loopTroughDirectory(PATH_8BIT_TEST, PATH_8BIT_TEST, loopTroughOutputDir)
    ff.loopTroughDirectory(PATH_4BIT_TEST, PATH_4BIT_TEST, loopTroughOutputDir)
    ff.loopTroughDirectory(PATH_2BIT_TEST, PATH_2BIT_TEST, loopTroughOutputDir)
    ff.loopTroughDirectory(PATH_1BIT_TEST, PATH_1BIT_TEST, loopTroughOutputDir)

    # Clean up images for better OCR
    ff.loopTroughDirectory(PATH_8BIT_TEST, PATH_8BIT_TEST, cleanUpImage)
    ff.loopTroughDirectory(PATH_4BIT_TEST, PATH_4BIT_TEST, cleanUpImage)
    ff.loopTroughDirectory(PATH_2BIT_TEST, PATH_2BIT_TEST, cleanUpImage)
    ff.loopTroughDirectory(PATH_1BIT_TEST, PATH_1BIT_TEST, cleanUpImage)

    # Make the ocr reading
    ff.loopTroughDirectory(PATH_8BIT_TEST, PATH_8BIT_TEST, googleOCR)
    ff.loopTroughDirectory(PATH_4BIT_TEST, PATH_4BIT_TEST, googleOCR)
    ff.loopTroughDirectory(PATH_2BIT_TEST, PATH_2BIT_TEST, googleOCR)
    ff.loopTroughDirectory(PATH_1BIT_TEST, PATH_1BIT_TEST, googleOCR)

    # Make the superUpscaling and ocr reading on the upscaled image
    ff.loopTroughDirectory(PATH_8BIT_TEST, PATH_8BIT_TEST, upscale)
    ff.loopTroughDirectory(PATH_4BIT_TEST, PATH_4BIT_TEST, upscale)
    ff.loopTroughDirectory(PATH_2BIT_TEST, PATH_2BIT_TEST, upscale)
    ff.loopTroughDirectory(PATH_1BIT_TEST, PATH_1BIT_TEST, upscale)


# Function should be used with the loopTroughDirectory function in FileFunctions
def loopTroughInputDir(filePath, fileName, pathOutput):

    for i in range(0, AMMOUNT_OF_STEPS):

        # the quality of the picture in pixels, 100 is orgininal quality
        qualityPercent = 100 - (i * PERCENT_TO_REDUCE)

        newPathOutput = pathOutput+str(qualityPercent)+'ppt/'

        ff.makeDirectory(newPathOutput)

        im = Image.open(filePath+fileName)

        croppedIm = imf.cropImage(im, SQUARE)
        greyIm = imf.makeGrayscale(croppedIm)

        reducedIm = imf.reduceQualityOfImage(greyIm, i * PERCENT_TO_REDUCE)

        colorDepth = pathOutput[-5]+pathOutput[-4]+pathOutput[-3]+pathOutput[-2]
        newName = nm.getProcessedFileName(fileName, qualityPercent, colorDepth)

        actualFilePath = newPathOutput+newName+"/"

        ff.makeDirectory(actualFilePath)

        imf.saveImageAsBMP(reducedIm, newName, actualFilePath)



def loopTroughOutputDir(path, fileName, _):

    if not fileName.endswith(".png"):

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

            index = fileName.find("bit_")
            depth = fileName[index-1]

            newName = nm.addFileSize(pureFileName, fileSizes)
            newName += ".png"

            if depth != "4":
                if depth == "1":
                    key = pureFileName.replace("1bit", "4bit")
                    pathBit4 = db.pathBit4[key]
                    oldBit4Name = db.oldBit4Name[key]
                    newBit4Name = db.newBit4Name[key]
                        
                    ff.renameFile(pathBit4, oldBit4Name+".png", newBit4Name)
                    ff.removeFile(pathBit4, oldBit4Name+".bmp")
                    ff.removeFile(pathBit4, oldBit4Name+".bin")

                ff.renameFile(path, pureFileName+".png", newName)
                ff.removeFile(path, pureFileName+".bmp")
                ff.removeFile(path, pureFileName+".bin")

            else:
                db.pathBit4[pureFileName] = path
                db.oldBit4Name[pureFileName] = pureFileName
                db.newBit4Name[pureFileName] = newName

            db.binSizes = {}
            db.bmpSizes = {}

def cleanUpImage(path, filename, _):

    if filename.endswith(".png"):
        # print(f'cleanUpImage -> path:\n{path}')
        # print(f'cleanUpImage -> filename: {filename}')

        im = Image.open(path+filename)
        invIm = imf.invertImage(im)

        if not "1bit" in filename:
            finalIm = imf.thresholdImage(invIm)
        else:
            finalIm = imf.thresholdImage(invIm, True)

        name = filename.replace(".png","")
        # print(f'cleanUpImage -> name: {name}')

        imf.saveImageAsPNG(finalIm, name, path)


def googleOCR(path, filename, _):
    
    ocrValue = gv.detect_text(path+filename)
    ocrValue = ocrValue.replace(' ','')
    ocrValue = ocrValue.replace('   ','')
    ocrValue = ocrValue.replace('\n','')

    splitFileName = filename.split('_', 2)
    fileName, facit, tail = splitFileName[0], splitFileName[1], splitFileName[2]
    newFilename = fileName + '_' + facit + '_' + ocrValue + '_' + tail
    ff.renameFile(path, filename, newFilename)
    

def getOcrValues(path, filename, _):

    if filename.endswith('.png'):
        file = ff.getAbsPath(path+filename)
        # ocrValue = tm.getImageOCR(file)

        # splitFileName = filename.split('_', 2)
        # fileName, facit, tail = splitFileName[0], splitFileName[1], splitFileName[2]
        # newFilename = fileName + '_' + facit + '_' + ocrValue + '_' + tail
        # ff.renameFile(path, filename, newFilename)


def upscale(path, filename, _):

    if filename.endswith('.png'):
        suFilename = imf.superUpscale(path, filename)
        ocrValue = gv.detect_text(path+suFilename)
        ocrValue = ocrValue.replace(' ','')
        ocrValue = ocrValue.replace('   ','')
        ocrValue = ocrValue.replace('\n','')

        newFilename = filename.replace(".png", f'_{ocrValue}')
        ff.renameFile(path, filename, newFilename+'.png')

        #TODO: move suFiles to separate folder once OCR reading has been done.
