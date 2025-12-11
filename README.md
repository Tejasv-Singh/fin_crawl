# FINCRAWL: Autonomous Filings + Disclosures Early-Warning System

Fincrawl is a hackathon-ready financial intelligence platform that ingests SEC filings and News RSS, processes them using RAG (Retrieval Augmented Generation), and flags high-risk events (bankruptcy, fraud, default) using an autonomous scoring engine.

## Features
- **Autonmous Ingestion**: Crawls SEC EDGAR (10-K, 8-K) and RSS feeds.
- **RAG & Vector Search**: Semantically indexes documents using ChromaDB and SentenceTransformers.
- **Risk Scoring**: Heuristic signal engine detects "material weakness", "going concern", and other red flags.
- **Dashboard**: React-based UI for real-time risk monitoring.

## Tech Stack
- **Backend**: Python (FastAPI), Celery (Worker), SQLite, ChromaDB (Vector Store).
- **Frontend**: React, Vite, TailwindCSS.
- **Infrastructure**: Local MVP mode (No Docker required).

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Setup Backend
```bash
# Create venv and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Setup Frontend
```bash
cd frontend
npm install
cd ..
```

### 3. Run Application
Use the Makefile for convenience:
```bash
make run-all
```
This will start:
- Backend API at `http://localhost:8001`
- Frontend Dashboard at `http://localhost:5173`

### 4. Trigger Ingestion
To start crawling data:
```bash
make crawl
```

### 5. Run Backtest
To validate the risk scoring logic:
```bash
make backtest
```

## Directory Structure
- `backend/`: FastAPI application and processing logic.
- `frontend/`: React dashboard.
- `scripts/`: Utility scripts (backtesting).

