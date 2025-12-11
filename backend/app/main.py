from fastapi import FastAPI, BackgroundTasks
from app.core.config import settings
from app.db.session import engine, Base
from app.worker.tasks import crawl_sec_edgar, crawl_rss_feed
from typing import List

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

@app.get("/")
def root():
    return {"message": "Welcome to FINCRAWL API"}

@app.post(f"{settings.API_V1_STR}/crawl/sec")
def trigger_sec_crawl(background_tasks: BackgroundTasks):
    crawl_sec_edgar.delay()
    return {"message": "SEC Crawl triggered"}

@app.post(f"{settings.API_V1_STR}/crawl/rss")
def trigger_rss_crawl(urls: List[str]):
    for url in urls:
        crawl_rss_feed.delay(url)
    return {"message": "RSS Crawl triggered"}
