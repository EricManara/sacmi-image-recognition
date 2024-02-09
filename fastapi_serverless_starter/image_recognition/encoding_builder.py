from numpy import ndarray
from sentence_transformers import SentenceTransformer
from torch import Tensor
from fastapi_serverless_starter.services import S3_service
from PIL import Image
import json
import os

print('Loading CLIP Model...')
CLIPmodel = SentenceTransformer('clip-ViT-B-32')

dirname = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(dirname, 'models\\')

def encodeImage(image):
    return CLIPmodel.encode(image, show_progress_bar=True)

def saveEncoding(encoding, typeID: str):
    file = open(os.path.join(model_path, typeID), "w")
    json.dump(encoding, file)

def appendEncoding(newEncoding: list[Tensor] | ndarray | Tensor, typeID: str):
    try:
        file = open(os.path.join(model_path, typeID), "rb+")
    except FileNotFoundError:
        file = open(os.path.join(model_path, typeID), "w")
        file.close()
        file = open(os.path.join(model_path, typeID), "rb+")
    file.seek(0, os.SEEK_END)
    print(file.tell())
    if file.tell() == 0:
        file.close()
        file = open(os.path.join(model_path, typeID), "w")
        file.write('['), file.write(json.dumps(newEncoding.tolist())), file.write(']')
        return
    file.seek(file.tell() - 1, os.SEEK_SET)
    file.truncate()
    file.close()
    file = open(os.path.join(model_path, typeID), "a")
    file.write(', ' + json.dumps(newEncoding.tolist()) + ']')

def appendImage(image, typeID: str):
    name = image.filename
    image = Image.open(image.file)
    encodedImage = encodeImage(image)
    appendEncoding(encodedImage, typeID)
    S3_service.saveImage(image, typeID, name)

def appendS3Image(imageID: str, typeID: str):
    encodedImage = encodeImage(S3_service.getImageByID(imageID))
    appendEncoding(encodedImage, typeID)

def buildEncoding(typeID: str):

    encodedImages = [encodeImage(image).tolist() for image in S3_service.getImagesByType(typeID)]

    saveEncoding(encodedImages, typeID)
