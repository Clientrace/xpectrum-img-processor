
from PIL import Image


def resize(base_width, img):
    img.convert('RGB')
    img_width, img_height = img.size

    ratio = (base_width/float(img_width))
    height = int((float(img_height) * float(ratio)))
    img = img.resize((base_width, height), Image.ANTIALIAS)
    img = img.convert('RGB')
    return img






