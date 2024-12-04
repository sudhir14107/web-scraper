from fastapi import APIRouter, Depends, Query
from ..services.scraper import ScraperService
from ..middlewares.auth import verify_token

router = APIRouter()

# Dependency injection for ScraperService
def get_scraper_service(page_limit: int = Query(5, ge=1), proxy: str = None):
    return ScraperService(page_limit=page_limit, proxy=proxy)

@router.get("/api/scrape", dependencies=[Depends(verify_token)])

async def scrape_endpoint(scraper_service: ScraperService = Depends(get_scraper_service)):
    result = scraper_service.start_scraping()
    return {"message": result}
