import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

class APIDiscoverer:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.api_endpoints = set()

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def crawl(self, url):
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return
            soup = BeautifulSoup(response.text, "html.parser")
            # Find all links
            for link in soup.find_all("a", href=True):
                href = link['href']
                full_url = urljoin(url, href)
                if self.is_valid_url(full_url) and full_url.startswith(self.base_url):
                    self.crawl(full_url)
            # Find potential API endpoints in scripts or page content
            self.find_api_endpoints(response.text)
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")

    def find_api_endpoints(self, text):
        # Regex to find URLs containing 'api' or 'rest'
        pattern = re.compile(r'https?://[^\s"\']*?(api|rest)[^\s"\']*', re.IGNORECASE)
        matches = pattern.findall(text)
        for match in matches:
            self.api_endpoints.add(match)

    def run(self):
        print(f"Starting crawl at {self.base_url}")
        self.crawl(self.base_url)
        print("Discovered API endpoints:")
        for endpoint in self.api_endpoints:
            print(endpoint)

if __name__ == "__main__":
    base_url = "https://www.equityshieldadvocates.com"
    discoverer = APIDiscoverer(base_url)
    discoverer.run()
