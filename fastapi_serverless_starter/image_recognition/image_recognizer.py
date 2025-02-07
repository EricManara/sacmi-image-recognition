from PIL import Image
from fastapi import UploadFile

from fastapi_serverless_starter.image_recognition import encoding_builder
from fastapi_serverless_starter.services import S3_service
from sentence_transformers import util
import numpy

def recognizeImage(queryImage: UploadFile, typeID: str):
    name = queryImage.filename
    queryImage = Image.open(queryImage.file)
    encodedImages = S3_service.loadEncoding(typeID)
    queryEncoding = encoding_builder.encodeImage(queryImage)

    for image in encodedImages:
        processed_images = util.paraphrase_mining_embeddings(numpy.array([image, queryEncoding]))
        print("Processed image: " + str(processed_images[0][0] * 100) + '%')
        if processed_images[0][0] > 0.92:
            
            S3_service.saveImage(queryImage, typeID, name)
            encoding_builder.appendEncoding(queryEncoding, typeID)

            return True
    return False
