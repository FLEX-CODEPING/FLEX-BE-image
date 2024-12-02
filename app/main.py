from fastapi import FastAPI, APIRouter, Body, Query
from fastapi.security import HTTPBearer
from app.config.swagger_config import setup_swagger
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from app.config.eureka_client import eureka_lifespan
from app.infra.minio_client import client
from app.common.common_response import CommonResponseDto
from minio.error import S3Error
import uuid


app = FastAPI(
    lifespan=eureka_lifespan,
    docs_url = "/api/image-service/swagger-ui.html",
    openapi_url = "/api/image-service/openapi.json",
    redoc_url="/api/image-service/redoc",
    title = "Image service"
)

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://do-flex.co.kr:3000",
    "http://dev.do-flex.co.kr:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

setup_swagger(app)
security = HTTPBearer()

expires = timedelta(seconds=3600)

@app.get("/api/presigned-url")
async def get_presigned_url(bucketName: str, fileName: str):
    """
    Presigned URL 생성
    - bucketName: S3 버킷 이름
    - fileName: 원본 파일명
    """
    try:
        unique_id = uuid.uuid4()
        
        new_file_name = f"{unique_id}_{fileName}"
        
        presigned_url = client.presigned_put_object(bucketName, new_file_name, expires=expires)
        
        return CommonResponseDto(result=presigned_url)
    except S3Error as err:
        return CommonResponseDto(result=str(err))