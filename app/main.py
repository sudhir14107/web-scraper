from fastapi import FastAPI
from app.routes.scraper import router as scraping_router

app = FastAPI()

# Include routes
app.include_router(scraping_router)