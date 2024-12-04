from fastapi import APIRouter, Depends
from ..services.scraper import ScraperService
from ..middlewares.auth import verify_token

router = APIRouter()

# Dependency injection for ScraperService
def get_scraper_service():
    return ScraperService()

@router.get("/api/scrape", dependencies=[Depends(verify_token)])

async def scrape_endpoint(scraper_service: ScraperService = Depends(get_scraper_service)):
    result = scraper_service.start_scraping()
    return {"message": result}
