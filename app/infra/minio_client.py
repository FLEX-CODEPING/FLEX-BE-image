from minio import Minio
from minio.error import S3Error
from app.config.app_config import settings

client = Minio(
    settings.minio_host,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=False  
)