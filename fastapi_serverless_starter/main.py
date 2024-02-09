from fastapi import FastAPI

from fastapi_serverless_starter.routers import health
from fastapi_serverless_starter.routers import img_recognition_api

app = FastAPI()


app.include_router(health.router)
app.include_router(img_recognition_api.router)
