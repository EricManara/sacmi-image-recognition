from fastapi import APIRouter, UploadFile, File
from fastapi_serverless_starter.image_recognition import encoding_builder, image_recognizer

router = APIRouter()

@router.post("/build_encoding")
async def buildEncoding(typeID: str):
    encoding_builder.buildEncoding(typeID)
    return {"status": "ok"}

@router.put("/add_S3_img")
async def addS3Img(imageID: str, typeID: str):
    encoding_builder.appendS3Image(imageID, typeID)
    return {"status": "ok"}

@router.put("/add_img")
async def addImg(typeID: str, image: UploadFile = File(...)):
    encoding_builder.appendImage(image, typeID)
    return {"status": "ok"}

@router.put("/recognize")
async def recognize(typeID: str, image: UploadFile = File(...)):
    return image_recognizer.recognizeImage(image, typeID)
