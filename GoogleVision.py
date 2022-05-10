import io
import os
# Imports the Google Cloud client library
from google.cloud import vision

document = True

def detect_text(path):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # text_detection 
    # document_text_detection
    if doc:
        response = client.document_text_detection(image=image)
    else:
        response = client.text_detection(image=image)


    texts = response.text_annotations

    # print('Texts:')

    # for text in texts:
    #     print('\n"{}"'.format(text.description))

    #     vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                 for vertex in text.bounding_poly.vertices])

    #     print('bounds: {}'.format(','.join(vertices)))

    if not response.error.message:
        try:
            return cleanOcrValue(texts[0].description)
        except:
            return ""
    else:
        print(f"\nGOOGLE VISION -> ERROR: \n{response.error.message}\n")
        return ""


def cleanOcrValue(value):
    value = value.replace(' ','')
    value = value.replace('   ','')
    value = value.replace('\n','')
    
    newValue = ""
    for char in value:

        if char.isdecimal():
            newValue += char
        else: 
            newValue += "x"

    return newValue