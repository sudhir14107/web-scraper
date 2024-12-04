from fastapi import APIRouter, Depends, Query
from ..services.scraper import ScraperService
from ..middlewares.auth import verify_token

router = APIRouter()

# Dependency injection for ScraperService
def get_scraper_service(page_limit: int = Query(5, ge=1), proxy: str = None, recipients: list = []):
    return ScraperService(proxy=proxy, page_limit=page_limit, recipients=recipients)

@router.get("/api/scrape")
async def scrape_endpoint(
    page_limit: int = 5, 
    proxy: str = None, 
    recipients: list = [], 
    scraper_service: ScraperService = Depends(get_scraper_service), 
    token: str = Depends(verify_token)
):
    try:
        result = scraper_service.start_scraping(page_limit)
        return {"message": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
