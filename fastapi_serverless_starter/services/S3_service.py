from PIL import Image
import boto3
import glob
import json
import os

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

dirname = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(dirname, 'models\\')

print("Connecting to AWS S3...")
s3 = boto3.resource(
    service_name='s3',
    region_name='eu-north-1',
    aws_access_key_id='AKIAT3UT3XOJA74QAP5P',
    aws_secret_access_key='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'
)
for bucket in s3.buckets.all():
    print(bucket.name)

def getImagesByType(typeID: str):
    images = list(glob.glob("C:/Users/snps/Projects/OpenCV-Maventest/src/main/resources/" + typeID + '/*.jpg'))
    return [Image.open(filepath) for filepath in images]

def getImageByID(imageID: str):
    return Image.open("C:/Users/snps/Projects/OpenCV-Maventest/src/main/resources/newImg/" + imageID + '.jpg')

def saveImage(image: Image, typeID: str, name: str):
    image.save("C:/Users/snps/Projects/OpenCV-Maventest/src/main/resources/" + typeID + '/' + name)
    return

def loadEncoding(typeID: str):
    print("Loading images encoding for type: " + typeID)
    file = open(os.path.join(model_path, typeID), 'r')
    return json.load(file)
