
import boto3
import botocore

class S3:

  def __init__(self, bucketName, awsCred=None):
    """
    Initialize S3
    """

    self.bucketName = bucketName
    if awsCred:
      self.S3_c = boto3.client(
        's3',
        aws_access_key_id = awsCred['aws_id'],
        aws_secret_access_key = awsCred['aws_secret'],
        region_name = 'ap-southeast-1'
      )
      self.S3_r = boto3.resource(
        's3',
        aws_access_key_id = awsCred['aws_id'],
        aws_secret_access_key = awsCred['aws_secret'],
        region_name = 'ap-southeast-1'
      )
    else:
      self.S3_c = boto3.client(
        's3',
        region_name = 'ap-southeast-1'
      )
      self.S3_r = boto3.resource(
        's3',
        region_name = 'ap-southeast-1'
      )

  def list_objects(self, prefix):
    """
    List s3 objects
    :param prefix: List object that starts with this prefix
    :type prefix: string
    :return: list of s3 objects
    :rtype: list of string
    """
    objectList = self.S3_c.list_objects(
      Bucket = self.bucketName,
      Prefix = prefix
    )
    return objectList


  def delete_resource(self, key):
    """
    Delete s3 object
    """

    resp = self.S3_c.delete_object(
      Bucket=self.bucketName,
      Key=key
    )
    return resp

  def does_file_exists(self, key):
    """
    Check if file exist
    """
    try:
      self.S3_r.Object(self.bucketName, key).load()
    except botocore.exceptions.ClientError as e:
      if e.response['Error']['Code'] == '404':
        return False
    return True

  def load_resource_content(self, key):
    """
    Load s3 resource
    :param key: resource full dir name
    :type key: string
    :returns: resource content
    :rtype: string
    """

    s3Object = self.S3_r.Object(self.bucketName, key)
    sContent = s3Object.get()['Body'].read().decode('utf-8')
    return sContent

  def load_resource_bytes(self, key):
    """
    Load s3 resource
    :param key: resource full dir name
    :type key: string
    :returns: resource content
    :rtype: string
    """

    s3Object = self.S3_r.Object(self.bucketName, key)
    sContent = s3Object.get()['Body'].read()
    return sContent

  def get_object(self, key):
    """
    Load s3 file
    :param key: resource full dir name
    :type key: string
    :returns: resource content
    :rtype: string
    """

    s3Object = self.S3_r.Object(self.bucketName, key)
    object = s3Object.get()['Body']
    return object
  
  def save_resource(self, key, body, cType='text/plain', public=False):
    """
    Save s3 resource
    :param key: resource full dir name
    :type key: string
    :param body: resource object content
    :type body: depends on the content type
    :param cType: resource content type
    :type cType: string
    """

    s3Object = self.S3_r.Object(self.bucketName, key)
    if public:
      s3Object.put(
        ContentType = cType,
        Body = body,
        ACL = 'public-read'
      )
    else:
      s3Object.put(
        ContentType = cType,
        Body = body
      )

  def move_file(self, dir1, dir2):
    """
    Move s3 file
    """
    self.S3_c.copy_object(
      Bucket = self.bucketName,
      CopySource = self.bucketName + '/' + dir1,
      Key = dir2,
      ACL = 'public-read'
    )

    self.delete_resource(dir1)


  def list_objects_v2(self, prefix, maxKeys=10, startToken = None):
    """
    List Object v2
    """

    operation_parameters = {
      'Bucket' : self.bucketName,
      'Prefix' : prefix,
      'MaxKeys' : maxKeys
    }

    if startToken:
      operation_parameters['ContinuationToken'] = startToken

    objList = self.S3_c.list_objects_v2(**operation_parameters)
    return objList


  def get_presigned_url(self, fname, method, ftype, expirationTyime=3600):
    """
    Generate presigned URL
    """
    http_method = (method == 'put_object') and 'PUT' or 'GET'
    if http_method == 'PUT':
      return  self.S3_c.generate_presigned_url(
        ClientMethod=method,
        HttpMethod=http_method,
        Params={
          'Bucket' : self.bucketName,
          'Key' : fname,
          'ContentType' : ftype,
          'ACL' : 'public-read'
        }
      )

    return  self.S3_c.generate_presigned_url(
      ClientMethod=method,
      HttpMethod=http_method,
      Params={
        'Bucket' : self.bucketName,
        'Key' : fname
      }
    )
  




