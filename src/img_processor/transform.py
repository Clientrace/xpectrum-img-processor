
from PIL import Image


def resize(base_width, img_blob):
    img = Image.open(img_blob)
    img_width, img_height = img.size

    ratio = (base_width/float(img_width))
    height = int((float(img_height) * float(ratio)))
    img = img.resize((base_width, height), Image.ANTIALIAS)
    return img






