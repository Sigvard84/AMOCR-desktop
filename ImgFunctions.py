from PIL import Image

def makeGrayscale(im):
    
    gsIm = im.convert('L')

    return gsIm
