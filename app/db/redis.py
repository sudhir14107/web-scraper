from dotenv import load_dotenv
import os
import redis
import logging

load_dotenv()

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisCache:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        try:
            # Get Redis connection details from environment variables
            redis_host = os.getenv("REDIS_HOST", "localhost")
            redis_port = int(os.getenv("REDIS_PORT", 6379))
            redis_db = int(os.getenv("REDIS_DB", 0))

            # Initialize Redis connection pool
            self.pool = redis.ConnectionPool(
                host=redis_host,
                port=redis_port,
                db=redis_db,
            )
            self.redis = redis.Redis(connection_pool=self.pool)
            
            # Try to ping Redis to check if the connection is alive
            self.redis.ping()
            logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
        
        except redis.ConnectionError as e:
            logger.error(f"Redis connection failed: {e}")
            raise ConnectionError(f"Could not connect to Redis at {os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}") from e

    def set(self, key, value, expiry=None):
        self.redis.set(key, value, ex=expiry)

    def get(self, key):
        return self.redis.get(key)
