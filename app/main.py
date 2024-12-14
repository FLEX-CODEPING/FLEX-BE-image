from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from app.infra.minio_client import get_minio_client
from app.common.common_response import CommonResponseDto
from minio.error import S3Error
import uuid
from app.infra.redis_config import get_redis
from urllib.parse import urlparse, urlunparse
from app.service.minio_image_scheduler import *
from app.lifespan import lifespan
from app.config.swagger_config import setup_swagger

app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/image-service/swagger-ui.html",
    openapi_url="/api/image-service/openapi.json",
    redoc_url="/api/image-service/redoc",
    title="Image service"
)

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://do-flex.co.kr:3000",
    "http://dev.do-flex.co.kr:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_swagger(app)
security = HTTPBearer()
expires = timedelta(seconds=3600)
scheduler = AsyncIOScheduler()  

@app.get("/api/presigned-url")
async def get_presigned_url(bucketName: str, fileName: str, redis=Depends(get_redis), minio_client=Depends(get_minio_client)):
    """
    Presigned URL 생성
    - bucketName: 버킷 이름, 블로그: dev-blog / 유저: dev-user
    - fileName: 원본 파일명
    """
    try:
        unique_id = uuid.uuid4()
        new_file_name = f"{unique_id}_{fileName}"
        
        presigned_url = minio_client.presigned_put_object(bucketName, new_file_name, expires=expires)
        parsed_url = urlparse(presigned_url)
        image_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
        
        await redis.set(image_url, "INACTIVE") 
        
        return CommonResponseDto(result=presigned_url)
    except S3Error as err:
        return CommonResponseDto(result=str(err))
