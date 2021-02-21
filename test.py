
from io import BytesIO
from src.img_processor import transform


img_data = None
with open('sample.jpg','rb') as img:
    img_data = BytesIO(img.read())

img_transformed = transform.resize(450, img_data)

out_io = BytesIO()
img_transformed.save(out_io, format='JPEG')

with open('o-sample.jpg','wb') as writer:
    writer.write(out_io.getvalue())






