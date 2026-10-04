import os
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv(override=True)
def init_redis(decode_responses=True):
    pool =  redis.ConnectionPool.from_url(url=os.getenv("REDIS_URL"),max_connections=10,decode_responses=decode_responses)
    redis_client = redis.Redis(connection_pool=pool)
    return redis_client