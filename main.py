from PIL import Image
import io
import os, sys
import ImgFunctions as imf
import FileFunctions as ff

PATH_ROBIN = "C:\Users\robin\Desktop\AMOCR-INPUT-FOLDER"
PATH_FREDRIK = "bmp_images/grayscale/"
inputPath = PATH_ROBIN


im = Image.open(input)

box = (130, 300, 270, 370)

cropedIm = imf.cropImage(im, box)

cropedIm.save()


 