import redis.asyncio as redis
from app.config.app_config import settings

redis_client = redis.StrictRedis(
        host=settings.redis_host, 
        port=settings.redis_port, 
        db=settings.redis_db, 
        decode_responses=True)

async def get_redis() -> redis.Redis:
    return redis_client
