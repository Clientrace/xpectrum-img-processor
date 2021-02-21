
import json
import src.aws.s3 import S3

def handler(event, context):
    """
    event:
        s3DirPrefix: Output Directory Image Prefix (folder) 
        base_width: Thumbnail base width
    """
    return {
        'statusCode': 200,
        'body': json.dumps({
            's3FileUrl': ''
        })
    }



