import requests
import sqlite3
import time

BASE_URL = "http://localhost:8001/api/v1"

def verify_step3():
    print("Verifying Step 3: Risk Scoring...")

    # 1. Trigger Crawl
    print("Triggering Crawl...")
    try:
        requests.post(f"{BASE_URL}/crawl/sec")
        print("Crawl request sent.")
    except Exception as e:
        print(f"Crawl failed: {e}")
        return

    # 2. Check DB for Scores
    print("Checking DB for Risk Scores...")
    conn = sqlite3.connect("fincrawl.db")
    c = conn.cursor()
    
    # Wait a bit if needed (but we are in eager mode so it should be done)
    c.execute("SELECT id, title, risk_score FROM documents ORDER BY risk_score DESC LIMIT 5")
    rows = c.fetchall()
    
    if not rows:
        print("FAIL: No documents found.")
    else:
        print(f"Found {len(rows)} documents.")
        for r in rows:
            print(f" - [{r[0]}] {r[1]} (Score: {r[2]})")
            if r[2] > 0:
                print("   PASS: Non-zero risk score found.")

    conn.close()

if __name__ == "__main__":
    verify_step3()
