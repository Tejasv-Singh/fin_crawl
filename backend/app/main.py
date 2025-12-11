from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
from app.worker.tasks import crawl_sec_edgar, crawl_rss_feed
from app.services.vector_db import vector_db
from app.db.models import Document
from app.db.session import SessionLocal
from typing import List, Optional

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get(f"{settings.API_V1_STR}/documents")
def list_documents(limit: int = 50):
    """
    List documents, sorted by risk score descending.
    """
    db = SessionLocal()
    try:
        docs = db.query(Document).order_by(Document.risk_score.desc()).limit(limit).all()
        return docs
    finally:
        db.close()

@app.get(f"{settings.API_V1_STR}/search")
def search_documents(query: str, limit: int = 5):
    """
    Semantic search over documents.
    """
    results = vector_db.query(query, n_results=limit)
    return results
