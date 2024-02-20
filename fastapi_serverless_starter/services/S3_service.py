from PIL import Image
import boto3
import json
import os
from io import BytesIO
from botocore.exceptions import ClientError

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

dirname = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(dirname, 'models-tmp/')

bucket_name = "s3connect-test"
print("Connecting to AWS S3...")
s3 = boto3.client(
    service_name='s3',
    region_name='eu-north-1',
    aws_access_key_id='AKIAT3UT3XOJA74QAP5P',
    aws_secret_access_key='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'
)

def getImagesByType(typeID: str):
    print("Fetching images for type:", typeID)
    objs = s3.list_objects(Bucket=bucket_name, Prefix=typeID+'/').get('Contents')
    if objs is None:
        print("No objects found for type:", typeID)
        return []
    imgNames = [obj.get('Key') for obj in objs]
    try:
        imgNames.remove(typeID+'/model')
    except ValueError:
        print("No model found for type:", typeID, ", starting first model build...")
    try:
        imgNames.remove(typeID + '/')
    except ValueError:
        None
    print("Downloading images...")
    images = [s3.get_object(Bucket=bucket_name, Key=name).get('Body').read() for name in imgNames]
    return [Image.open(BytesIO(image)) for image in images]

def getImageByID(typeID: str, imageID: str):
    return Image.open(BytesIO(s3.get_object(Bucket=bucket_name, Key=typeID+'/'+imageID).get('Body').read()))

def saveImage(image: Image, typeID: str, name: str):
    tmpImg = BytesIO()
    image.save(tmpImg, format=image.format)
    tmpImg.seek(0)
    s3.upload_fileobj(tmpImg, bucket_name, typeID+'/'+name)

def saveEncoding(encoding, typeID: str):
    s3.upload_fileobj(encoding, bucket_name, typeID+'/model')
    print("Encoding saved")

def loadEncoding(typeID: str):
    print("Loading images encoding for type:", typeID)
    path = os.path.join(model_path, typeID)
    try:
        file = open(path, 'wb+')
        s3.download_fileobj(Bucket=bucket_name, Key=typeID+'/model', Fileobj=file)
        file.close()
    except ClientError:
        print("Could not download encoding for type:", typeID, ", creating new encoding...")
        return []
    file = open(path, 'r')
    encoding = json.load(file)
    file.close()
    return encoding
