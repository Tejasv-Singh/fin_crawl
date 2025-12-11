import feedparser
from typing import List, Dict

class RSSCrawler:
    @staticmethod
    def fetch_feed(feed_url: str) -> List[Dict]:
        feed = feedparser.parse(feed_url)
        results = []
        for entry in feed.entries:
            results.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")
            })
        return results
