import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time


class LinkScraper:
    ua = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
    }

    def __init__(self, urls):
        self.urls = urls
        self.session = requests.Session()
        self.session.headers.update(self.ua)
        self.links = self.scrape_links(urls)
        self.link_count = self.export_links()

    def filter_link(self, link):
        keys = [
            "bitcointalk.org",
            "www.simplemachines.org",
            "bitcoin.org",
            "w3.org",
            "www.privateinternetaccess.com",
            "www.mysql.com",
            "www.php.net",
            "www.redditblog.com",
            "reddit.com",
            "redditgifts.com",
            "www.reddithelp.com",
        ]
        for key in keys:
            if key in link:
                return False
        if link:
            return True

    def scrape_links(self, urls):
        all_links = []
        for url in urls:
            resp = self.session.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            raw_links = [link.get("href") for link in soup.find_all("a")]
            links = [urlparse(link).netloc for link in raw_links]
            links = list(filter(self.filter_link, set(links)))
            all_links.append(links)
        return all_links

    def export_links(self):
        for link_group in self.links:
            with open("links.txt", "r") as f:
                links = [link.strip() for link in f.readlines()]
            f.close()
            with open("links.txt", "a+") as f:
                for link in link_group:
                    if link not in links:
                        f.write("\n" + link)
            f.close()
        return len(links)


if __name__ == "__main__":
    urls = [
        "http://bit.ly/2Q1vJk5",
        "http://bit.ly/2JItFMu",
    ]  # Shortened for readability
    while True:
        try:
            print("[Links]: {}".format(LinkScraper(urls).link_count))
            time.sleep(10)
        except:
            pass
