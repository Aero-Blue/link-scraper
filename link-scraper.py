import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time
import configparser
import random


class LinkScraper:
    def __init__(self):
        self.ua = {"User-Agent": config["DEFAULT"]["UserAgent"]}
        self.urls = config["DEFAULT"]["URLs"].split(",\n")
        self.keys = config["DEFAULT"]["Filters"].split(",\n")
        self.session = requests.Session()
        self.session.headers.update(self.ua)
        self.links = self.scrape_links(self.urls)
        self.link_count = self.export_links()

    def filter_link(self, link):
        for key in self.keys:
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


class Main:
    def __init__(self):
        config.read("config.ini")
        while True:
            try:
                self.update_count()
            except:
                pass

    def update_count(self):
        freq = int(config["DEFAULT"]["UpdateFrequency"])
        link_count = LinkScraper().link_count
        print("[Links]: {}".format(link_count))
        time.sleep(freq)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    Main()
