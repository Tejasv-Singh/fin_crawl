from bs4 import BeautifulSoup
import requests

class BasicParser:
    @staticmethod
    def parse_html(html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Simple text extraction for MVP
        text = soup.get_text(separator='\n')
        return text

    @staticmethod
    def parse_url(url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BasicParser.parse_html(response.text)
        except Exception as e:
            print(f"Error parsing URL {url}: {e}")
            return ""
