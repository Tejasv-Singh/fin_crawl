import sqlite3
import os
import time

def verify():
    print("Verifying Step 1...")
    
    # Check DB
    if not os.path.exists("fincrawl.db"):
        print("FAIL: fincrawl.db not found.")
        return
    
    conn = sqlite3.connect("fincrawl.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT count(*) FROM documents")
        count = cursor.fetchone()[0]
        print(f"Documents in DB: {count}")
        
        if count > 0:
            cursor.execute("SELECT title, url, raw_s3_key FROM documents LIMIT 5")
            rows = cursor.fetchall()
            for r in rows:
                print(f" - {r[0]} ({r[1]})")
                # Check file content
                if r[2] and os.path.exists(r[2]):
                    size = os.path.getsize(r[2])
                    print(f"   Key: {r[2]} (Size: {size} bytes)")
                    with open(r[2], 'r', encoding='utf-8', errors='ignore') as f:
                        print(f"   Snippet: {f.read(100)}...")
                else:
                    print(f"   MISSING FILE: {r[2]}")
        else:
            print("WARN: No documents found in DB yet.")

    except Exception as e:
        print(f"FAIL: DB Query error: {e}")
    finally:
        conn.close()

    # Check Local Storage
    if not os.path.exists("local_data"):
        print("WARN: local_data directory not found.")
    else:
        files = os.listdir("local_data")
        print(f"Files in local_data: {len(files)}")
        if len(files) > 0:
            print(f" - Sample: {files[0]}")

if __name__ == "__main__":
    verify()
