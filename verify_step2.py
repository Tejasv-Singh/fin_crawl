import requests
import sqlite3
import time

BASE_URL = "http://localhost:8001/api/v1"

def verify_step2():
    print("Verifying Step 2: RAG Pipeline...")

    # 1. Trigger Crawl (which triggers embedding)
    print("Triggering Crawl...")
    try:
        requests.post(f"{BASE_URL}/crawl/sec")
        # Since eager mode, it finishes immediately?
        # Actually eager mode runs synchronously. So the request might hang until done?
        # Or celery.delay returns immediately but runs in the same thread?
        # In eager mode, .delay() blocks until task is done.
        # But `crawl_sec_edgar` is a task. Inside it, it calls `process_document.delay()`.
        # So yes, it should block.
        print("Crawl request returned.")
    except Exception as e:
        print(f"Crawl failed: {e}")
        return

    # 2. Check DB Status
    conn = sqlite3.connect("fincrawl.db")
    c = conn.cursor()
    c.execute("SELECT id, title, status FROM documents WHERE status='EMBEDDED' LIMIT 5")
    rows = c.fetchall()
    print(f"Embedded Documents: {len(rows)}")
    for r in rows:
        print(f" - [{r[0]}] {r[1]} ({r[2]})")
    conn.close()

    # 3. Test Search
    print("\nTesting Search for 'revenue'...")
    try:
        resp = requests.get(f"{BASE_URL}/search?query=revenue&limit=3")
        results = resp.json()
        print("Search Results:")
        # Chroma returns dict with 'documents', 'metadatas', etc.
        docs = results.get('documents', [[]])[0]
        parsed_metas = results.get('metadatas', [[]])[0]
        
        for i, doc in enumerate(docs):
            meta = parsed_metas[i]
            print(f"Rank {i+1}: {meta.get('title')} (Doc ID: {meta.get('doc_id')})")
            print(f"Snippet: {doc[:100]}...")
            print("-" * 20)
            
    except Exception as e:
        print(f"Search failed: {e}")

if __name__ == "__main__":
    verify_step2()
