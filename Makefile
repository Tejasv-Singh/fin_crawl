.PHONY: setup run-backend run-frontend run-all crawl backtest clean

setup:
	python3 -m venv venv
	venv/bin/pip install -r backend/requirements.txt
	cd frontend && npm install

run-backend:
	venv/bin/uvicorn app.main:app --app-dir backend --reload --port 8001

run-frontend:
	cd frontend && npm run dev

run-all:
	@echo "Starting Backend & Frontend..."
	make run-backend & make run-frontend

crawl:
	curl -X POST http://localhost:8001/api/v1/crawl/sec
	curl -X POST http://localhost:8001/api/v1/crawl/rss -H "Content-Type: application/json" -d '["http://feeds.bbci.co.uk/news/business/rss.xml"]'

backtest:
	venv/bin/python scripts/backtest_scoring.py

clean:
	rm -rf fincrawl.db local_data chroma_db
