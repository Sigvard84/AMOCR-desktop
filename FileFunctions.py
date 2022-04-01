from os import path
import os
import sys
from pathlib import Path

def getAbsPath(relative_path):
    """ Returns the absolute path to resource, works for dev and for PyInstaller """

    base_path = getattr(sys, '_MEIPASS', Path().absolute())
    return path.join(base_path, relative_path)

def makeDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def loopTroughDirectory(pathInput, pathOutput, loopFunction):
    for filename in os.listdir(pathInput):
        
        if filename.endswith(".bmp"):
            print('loopTroughDirectory ->On file: ' + filename)
            loopFunction(pathInput, filename, pathOutput)