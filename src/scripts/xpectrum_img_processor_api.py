
import json

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




