from PIL import Image


def imageResizeing(width, height, image):
    resizedImage = image.resize((width, height), Image.BILINEAR)
    return resizedImage