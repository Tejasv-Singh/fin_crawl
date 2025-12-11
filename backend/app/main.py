from fastapi import FastAPI, BackgroundTasks
from app.core.config import settings
from app.db.session import engine, Base
from app.worker.tasks import crawl_sec_edgar, crawl_rss_feed
from app.services.vector_db import vector_db
from typing import List, Optional

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

@app.get(f"{settings.API_V1_STR}/search")
def search_documents(query: str, limit: int = 5):
    """
    Semantic search over documents.
    """
    results = vector_db.query(query, n_results=limit)
    return results
