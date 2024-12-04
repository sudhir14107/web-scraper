from fastapi import APIRouter, Depends, Query
from app.services.scraper import ScraperService
from app.db.redis import RedisCache
from app.dependencies import get_redis_cache  # Import Redis dependency
from ..middlewares.auth import verify_token

router = APIRouter()

# Dependency injection for ScraperService
def get_scraper_service(
    page_limit: int = Query(5, ge=1), 
    proxy: str = Query(None), 
    recipients: list = Query([]),  # Default empty list if not provided
    redis_cache: RedisCache = Depends(get_redis_cache)  # Redis injected here
) -> ScraperService:
    return ScraperService(redis_cache=redis_cache, page_limit=page_limit, proxy=proxy, recipients=recipients)

@router.get("/api/scrape")
async def scrape_endpoint(
    scraper_service: ScraperService = Depends(get_scraper_service),
    token: str = Depends(verify_token)
):
    try:
        result = scraper_service.start_scraping(scraper_service.page_limit)
        return {"message": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
