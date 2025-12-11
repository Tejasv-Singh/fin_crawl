from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.db.session import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)  # e.g., "SEC_EDGAR", "RSS_NEWS"
    doc_type = Column(String, index=True) # e.g., "10-K", "Article"
    company_tkr = Column(String, index=True, nullable=True)
    url = Column(String, unique=True, index=True)
    published_date = Column(DateTime(timezone=True))
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Storage paths
    raw_s3_key = Column(String, nullable=True) # Path in MinIO
    
    # Metadata
    title = Column(String, nullable=True)
    extra_metadata = Column(JSON, nullable=True)

    # Simple processing status
    status = Column(String, default="COLLECTED") # COLLECTED, PARSED, EMBEDDED
    
    # Risk Score
    risk_score = Column(Integer, default=0)
