
import io
import os
import json
from src.aws.s3 import S3
from src.img_processor import transform

global BASE_WIDTH
BASE_WIDTH = 450

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
    image_raw = s3.load_resource_bytes(key=event['s3ImgDir'])
    img_input = io.BytesIO(image_raw)
    img_output = io.BytesIO()


    img_transformed = transform.resize(BASE_WIDTH, img_input)
    img_transformed.save(img_output)

    s3_output_dir = 'thumbnail_'+event['s3ImgDir'].split('/')[-1]
    s3.save_resource(s3_output_dir, img_output.getvalue(), event['cType'] )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'msg': 'OK'
        })
    }


