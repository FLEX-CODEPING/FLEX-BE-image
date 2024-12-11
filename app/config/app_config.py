from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    app_env: str = "local"
    eureka_server_url: str
    app_name: str
    instance_host: str
    instance_port: int

    minio_host: str
    minio_access_key: str
    minio_secret_key: str
    blog_bucket: str
    user_bucket: str
    minio_secure: bool

    redis_host: str
    redis_port: int
    redis_db: str
    redis_password: str

    model_config = SettingsConfigDict(
        env_file="image-service.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

env = os.getenv("APP_ENV", "local")
settings = Settings(_env_file="image-service.env")