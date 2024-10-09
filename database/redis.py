import aioredis
from config import load_config

config = load_config()

redis = None

async def init_redis():
    global redis
    redis = await aioredis.create_redis_pool(
        (config.redis.host, config.redis.port)
    )

async def close_redis():
    redis.close()
    await redis.wait_closed()
