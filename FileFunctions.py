from os import path
import os
import sys
from pathlib import Path
import shutil
from tkinter import N
from zipfile import ZipFile

def getAbsPath(relative_path):
    """ Returns the absolute path to resource, works for dev and for PyInstaller """

    base_path = getattr(sys, '_MEIPASS', Path().absolute())
    return path.join(base_path, relative_path)

def makeDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def loopTroughDirectory(pathInput, pathOutput, loopFunction):
    for filename in os.listdir(pathInput):

        if os.path.isdir(pathInput+filename):
            #print("loopTroughDirectory -> Found dir: "+filename)
            loopTroughDirectory(pathInput+filename+"/", pathOutput, loopFunction)
        
        elif filename.endswith(".bmp") or filename.endswith(".bin") or filename.endswith(".png"):
            print('\nloopTroughDirectory -> On file: ' + filename)
            print('loopTroughDirectory -> Running function: ' + str(loopFunction).split(' ')[1])
            loopFunction(pathInput, filename, pathOutput)
            

def getFileSize(path, fileName):
    return os.path.getsize(path+fileName)

def zip(path, fileName):
    shutil.make_archive(fileName, "zip", path)

def removeFile(path, fileName):
    if os.path.exists(path+fileName):
        os.remove(path+fileName)

def removeDirectory(path):
    os.rmdir(path)

def renameFile(path, orgFilename, newFilename):
    os.rename(path+orgFilename, path+newFilename)

def copyFile(orgPath, fileName, newPath, newFilename):
    shutil.copy2(orgPath+fileName, newPath+newFilename)
