
import io
import os
import json
from src.aws.s3 import S3
from src.img_processor import transform

global BASE_WIDTH
BASE_WIDTH = 700

def handler(event, context):
    global BASE_WIDTH

    """
    event:
        cType: image content/mime type
        s3ImgDir: s3 image input directory
        baseWidth: Thumbnail base width
    """

    BASE_WIDTH = event['baseWidth']

    s3 = S3(
        bucketName = os.environ['bucketname']
    )
    print(event)
    image_raw = s3.load_resource_bytes(key=event['s3ImgDir'])
    img_input = io.BytesIO(image_raw)
    img_output = io.BytesIO()


    img_transformed = transform.resize(BASE_WIDTH, img_input)
    img_transformed.save(img_output, 'JPEG')

    s3_img_dir = event['s3ImgDir'].split('/')
    s3_output_dir = 'media/thumbnails/'+ event['group'] +'/'.join(s3_img_dir[2:])

    s3.save_resource(
        s3_output_dir,
        img_output.getvalue(),
        event['cType'],
        True
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'msg': 'OK'
        })
    }



