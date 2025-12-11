from app.worker.celery_app import celery_app
from app.crawlers.sec_edgar import SecEdgarCrawler
from app.crawlers.rss import RSSCrawler
from app.parsers.basic import BasicParser
from app.services.storage import storage
from app.db.session import SessionLocal
from app.db.models import Document
from datetime import datetime
import requests
import os
from app.core.config import settings
from app.services.vector_db import vector_db
from app.services.embedding import embedding_service

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
                if exists.status == "COLLECTED":
                     print(f"Triggering processing for existing doc {exists.id}")
                     process_document.delay(exists.id)
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
                db.refresh(doc) # Get ID
                print(f"Processed SEC filing: {filing['title']}")
                
                # Trigger Processing
                process_document.delay(doc.id)
                
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
                if exists.status == "COLLECTED":
                     process_document.delay(exists.id)
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
                db.refresh(doc)
                print(f"Processed RSS item: {item['title']}")
                
                # Trigger Processing
                process_document.delay(doc.id)

    finally:
        db.close()

@celery_app.task
def process_document(doc_id: int):
    """
    Reads document content, chunks it, embeds it, and saves to Vector DB.
    """
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            print(f"Document {doc_id} not found.")
            return
        
        if doc.status == "EMBEDDED":
            print(f"Document {doc_id} already embedded.")
            return

        # Read content
        content = ""
        # Local storage read
        if settings.USE_LOCAL_STORAGE:
             if doc.raw_s3_key and os.path.exists(doc.raw_s3_key):
                 with open(doc.raw_s3_key, 'r', encoding='utf-8', errors='ignore') as f:
                     content = f.read()
        else:
            # MinIO read placeholder (not implemented for MVP as we switched to local)
            pass
        
        if not content:
            print(f"No content for document {doc_id}")
            return

        # Chunk
        print(f"Chunking document {doc_id}...")
        chunks = embedding_service.split_text(content)
        
        if not chunks:
            print("No chunks generated.")
            return

        # Embed & Store
        # ChromaDB expects IDs. We'll generate simple ones.
        ids = [f"doc_{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"doc_id": doc_id, "source": doc.source, "title": doc.title, "url": doc.url} for _ in chunks]
        
        print(f"Adding {len(chunks)} chunks to Vector DB...")
        vector_db.add_chunks(chunks, metadatas, ids)
        
        doc.status = "EMBEDDED"
        db.commit()
        print(f"Successfully embedded document {doc_id}.")
        
    except Exception as e:
        print(f"Error processing document {doc_id}: {e}")
    finally:
        db.close()
