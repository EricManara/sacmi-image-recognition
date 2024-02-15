from sentence_transformers import SentenceTransformer, losses
from fastapi_serverless_starter.services import S3_service
from PIL import Image
import json
import os

print('Loading CLIP Model...')
CLIPmodel = SentenceTransformer('clip-ViT-B-32')  # clip-ViT-B-32 | clip-ViT-B-16 | clip-ViT-L-14

dirname = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(dirname, 'models-tmp/')

def encodeImage(image):
    return CLIPmodel.encode(image, show_progress_bar=True)

def saveEncoding(encoding, typeID: str):
    print("Saving encoding...")
    path = os.path.join(model_path, typeID)
    file = open(path, "w")
    json.dump(encoding, file)
    file.close()
    file = open(path, "rb")
    S3_service.saveEncoding(file, typeID)
    file.close()
    os.remove(path)

def appendEncoding(newEncoding, typeID: str):
    encodedImages = S3_service.loadEncoding(typeID)
    encodedImages.append(newEncoding.tolist())
    saveEncoding(encodedImages, typeID)

def appendImage(image, typeID: str):
    name = image.filename
    image = Image.open(image.file)
    encodedImage = encodeImage(image)
    appendEncoding(encodedImage, typeID)
    S3_service.saveImage(image, typeID, name)

def appendS3Image(imageID: str, typeID: str):
    encodedImage = encodeImage(S3_service.getImageByID(typeID, imageID))
    appendEncoding(encodedImage, typeID)

def buildEncoding(typeID: str):
    encodedImages = [encodeImage(image).tolist() for image in S3_service.getImagesByType(typeID)]
    saveEncoding(encodedImages, typeID)
