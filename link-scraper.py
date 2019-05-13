import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time


class LinkScraper:
    def __init__(self):
        self.session = requests.Session()
        self.links = self.scrape_links()

    def filter_link(self, link):
        keys = [
            "bitcointalk.org",
            "www.simplemachines.org",
            "bitcoin.org",
            "w3.org",
            "www.privateinternetaccess.com",
            "www.mysql.com",
            "www.php.net",
        ]
        for key in keys:
            if key in link:
                return False
        if link:
            return True

    def scrape_links(self):
        resp = self.session.get("https://bitcointalk.org/index.php?action=recent")
        soup = BeautifulSoup(resp.text, "html.parser")
        raw_links = [link.get("href") for link in soup.find_all("a")]
        print(raw_links)
        links = [urlparse(link).netloc for link in raw_links]
        links = list(filter(self.filter_link, set(links)))
        return links

    def export_links(self):
        with open("links.txt", "r") as f:
            links = [link.strip() for link in f.readlines()]
        f.close()
        with open("links.txt", "a+") as f:
            for link in self.links:
                if link not in links:
                    f.write("\n" + link)
        f.close()
        return len(links)


if __name__ == "__main__":
    while True:
        try:
            print(
                "[Links]: {}".format(LinkScraper().export_links()), flush=True, end="\r"
            )
            time.sleep(10)
        except:
            pass
