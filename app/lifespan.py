from fastapi import FastAPI
from app.infra.redis_config import get_redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from pytz import timezone
from app.config.eureka_client import eureka_lifespan 
from app.infra.minio_client import get_minio_client
from app.service.minio_image_scheduler import clean_inactive_images
scheduler = AsyncIOScheduler()
redis_client = None 

from fastapi import FastAPI
from app.infra.redis_config import get_redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from pytz import timezone
from app.config.eureka_client import eureka_lifespan 
from app.infra.minio_client import get_minio_client
from app.service.minio_image_scheduler import clean_inactive_images

scheduler = AsyncIOScheduler()
redis_client = None 

async def schedule_clean_inactive_images():
    minio_client = get_minio_client() 
    await clean_inactive_images(redis_client, minio_client)

async def lifespan(app: FastAPI):
    global redis_client
    
    redis_client = await get_redis()  

    async with eureka_lifespan(app): 
        scheduler.add_job(
            schedule_clean_inactive_images,
            CronTrigger(hour=0, minute=0, timezone=timezone('Asia/Seoul')),
            id='clean_inactive_images_job'
        )
    
        scheduler.start()  

        yield  

    scheduler.shutdown()  
    await redis_client.close()