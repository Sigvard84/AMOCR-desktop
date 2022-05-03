from tesserocr import PyTessBaseAPI, RIL

def getImageOCR(image):

    with PyTessBaseAPI() as api:
        api.SetImage(image)
        api.SetVariable('tessedit_char_whitelist', '0123456789')

        return api.GetUTF8Text()


