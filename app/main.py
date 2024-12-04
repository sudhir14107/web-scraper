from fastapi import FastAPI
from app.routes.scraper import router as scraping_router
from app.db.redis import RedisCache

app = FastAPI()

# Initialize RedisCache (configuration is read from environment variables)
redis_cache = RedisCache()

# Include routes
app.include_router(scraping_router)

# Pass redis_cache to the app state
app.state.redis_cache = redis_cache
