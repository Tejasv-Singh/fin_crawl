from app.worker.celery_app import celery_app
from app.crawlers.sec_edgar import SecEdgarCrawler
from app.crawlers.rss import RSSCrawler
from app.parsers.basic import BasicParser
from app.services.storage import storage
from app.db.session import SessionLocal
from app.db.models import Document
from datetime import datetime
import requests

@celery_app.task
def crawl_sec_edgar():
    crawler = SecEdgarCrawler()
    filings = crawler.fetch_latest_filings()
    
    db = SessionLocal()
    try:
        for filing in filings:
            # Check if exists
            exists = db.query(Document).filter(Document.url == filing['link']).first()
            if exists:
                continue

            # Download content (Basic HTML for now)
            try:
                headers = {'User-Agent': 'TejasvSingh tejasvhada1@gmail.com'}
                resp = requests.get(filing['link'], headers=headers)
                content = resp.content
                
                # Store raw
                filename = f"sec_{filing['id'].split(':')[-1]}.html" # Simple unique ID
                s3_key = storage.upload_content(filename, content, "text/html")
                
                # Parse (simple text)
                text_content = BasicParser.parse_html(content.decode('utf-8', errors='ignore'))
                
                # Save to DB
                doc = Document(
                    source="SEC_EDGAR",
                    doc_type="10-K", # Hardcoded for now based on crawler URL
                    url=filing['link'],
                    title=filing['title'],
                    published_date=datetime.now(), # Needs parsing, skip for MVP speed
                    raw_s3_key=s3_key,
                    extra_metadata={"summary": filing['summary']},
                    status="COLLECTED"
                )
                db.add(doc)
                db.commit()
                print(f"Processed SEC filing: {filing['title']}")
                
            except Exception as e:
                print(f"Error processing filing {filing['link']}: {e}")
                
    finally:
        db.close()

@celery_app.task
def crawl_rss_feed(url: str):
    crawler = RSSCrawler()
    items = crawler.fetch_feed(url)
    
    db = SessionLocal()
    try:
        for item in items:
             # Check if exists
            exists = db.query(Document).filter(Document.url == item['link']).first()
            if exists:
                continue
            
            # For RSS, we might just store metadata first, or crawl content immediately.
            # Lets crawl content immediately for MVP
            text = BasicParser.parse_url(item['link'])
            
            if text:
                # Upload raw text (or we could upload html if we fetched it raw)
                filename = f"rss_{hash(item['link'])}.txt"
                s3_key = storage.upload_content(filename, text.encode('utf-8'), "text/plain")
                
                doc = Document(
                    source="RSS",
                    doc_type="Article",
                    url=item['link'],
                    title=item['title'],
                    published_date=datetime.now(),
                    raw_s3_key=s3_key,
                    status="COLLECTED"
                )
                db.add(doc)
                db.commit()
                print(f"Processed RSS item: {item['title']}")

    finally:
        db.close()
