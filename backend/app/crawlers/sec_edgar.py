import requests
import feedparser
from typing import List, Dict

class SecEdgarCrawler:
    BASE_RSS_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=10-K&company=&dateb=&owner=include&start=0&count=40&output=atom"

    @staticmethod
    def fetch_latest_filings(count: int = 10) -> List[Dict]:
        headers = {'User-Agent': 'TejasvSingh tejasvhada1@gmail.com'} # SEC requires email in User-Agent
        response = requests.get(SecEdgarCrawler.BASE_RSS_URL, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch SEC RSS: {response.status_code}")
            return []

        feed = feedparser.parse(response.content)
        results = []
        for entry in feed.entries[:count]:
            results.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("updated", ""), # Atom uses updated
                "summary": entry.get("summary", ""),
                "id": entry.get("id", "")
            })
        return results
