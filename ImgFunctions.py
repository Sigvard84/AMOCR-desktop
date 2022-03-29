from PIL import Image

def makeGrayscale(im):
    
    gsIm = im.convert('L')

    return gsIm

def cropImage(im: Image, box):

    cropImage = im.crop(box)

    return cropImage
