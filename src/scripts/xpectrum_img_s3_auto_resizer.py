
import os
import json
from src.aws.s3 import S3


def handler(event, context):
    s3 = S3(
        bucketName = os.environ['bucketname']
    )
    s3_event = event['Records'][0]['s3']
    file_obj_key = s3_event['object']['key']
    image_raw = s3.load_resource_bytes(
        key = file_obj_key
    )




