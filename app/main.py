from fastapi import FastAPI, APIRouter, Body, Query
from fastapi.security import HTTPBearer
from app.config.swagger_config import setup_swagger
from fastapi.middleware.cors import CORSMiddleware
from app.config.eureka_client import eureka_lifespan


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