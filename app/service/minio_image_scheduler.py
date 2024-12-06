from app.config.app_config import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()
redis_client = None 
minio_client = None


def delete_image_from_minio(minio_client, image_url):
    blog_bucket_name = settings.blog_bucket
    try:
        object_key = "test"
        minio_client.remove_object(bucket_name=blog_bucket_name, object_name=object_key)
        print(f"Deleted image {object_key} from MinIO.")
    except Exception as e:
        print(f"Error deleting image {object_key}: {e}")

async def clean_inactive_images(redis, minio):
    print("Cleaning inactive images...")
    
    inactive_images = []
    
    keys = await redis.keys("*")  
   
    print(f"Keys found in Redis: {keys}")
    
    pipe = redis.pipeline()
    
    for key in keys:
        pipe.get(key)

    results = await pipe.execute() 

    print(f"Results from Redis GET commands: {results}")
    
    for i, result in enumerate(results):
        print(f"Key: {keys[i]}, Value: {result}") 
        if result == "INACTIVE":  
            inactive_images.append(keys[i]) 

    for image_url in inactive_images:
        delete_image_from_minio(minio, image_url) 
        await redis.delete(image_url) 