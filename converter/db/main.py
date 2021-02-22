import asyncio

import aioredis
from aiohttp.web_app import Application


async def setup_redis(app: Application):
    """
    Подключение к redis
    """
    redis = await aioredis.create_redis_pool(('redis', 6379),
                                             encoding='utf-8')
    app['redis'] = redis
    try:
        yield
    finally:
        redis.close()
        await redis.wait_closed()
