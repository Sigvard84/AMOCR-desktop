from PIL import Image
import io
import os, sys
import ImgFunctions as imf
import FileFunctions as ff

# orgPath = 'bmp_images/picture231.bmp'
# orgIm = Image.open(orgPath)

# gsIm = imf.makeGrayscale(orgIm)

# folderTup = os.path.split(orgPath)

# outfile = ff.getAbsPath(folderTup[0] + '/grayscale/' + folderTup[1])
# gsIm.save(outfile)


greyPath = 'bmp_images/grayscale/picture231.bmp'
greyIm = Image.open(greyPath)

box = (130, 300, 270, 370)
region = greyIm.crop(box)

greyFolderTup = os.path.split(greyPath)
cropOutfile = ff.getAbsPath(greyFolderTup[0] + '/cropped/' + greyFolderTup[1])

region.save(cropOutfile)


 