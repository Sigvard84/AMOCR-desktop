from tesserocr import PyTessBaseAPI
from PIL import Image

def getImageOCR(image):

    im = Image.open(image)

    with PyTessBaseAPI(psm=7) as api:
        api.SetImage(im)
        api.SetVariable('tessedit_char_whitelist', '0123456789')

        ocrResult = api.GetUTF8Text()

        return ocrResult.strip()


