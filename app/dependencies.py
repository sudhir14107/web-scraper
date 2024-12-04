from fastapi import Depends
from app.db.redis import RedisCache

# Dependency to inject RedisCache
def get_redis_cache() -> RedisCache:
    # Assuming RedisCache is already initialized elsewhere in your app
    return RedisCache()
