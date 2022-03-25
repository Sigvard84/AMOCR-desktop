from os import path
import sys
from pathlib import Path

def getAbsPath(relative_path):
    """ Returns the absolute path to resource, works for dev and for PyInstaller """

    base_path = getattr(sys, '_MEIPASS', Path().absolute())
    return path.join(base_path, relative_path)