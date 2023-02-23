import sys
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup


class CrawlerBase(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self):
        pass


class LinkCrawler(CrawlerBase):
    def __init__(self, genre, url):
        self.genre = genre
        self.url = url

    @staticmethod
    def get_page(url, page=1):
        try:
            res = requests.get(url + str(page))
        except:
            return None
        return res

    @staticmethod
    def find_links(html_doc):
        soup = BeautifulSoup(html_doc, "html.parser")
        div_tags = soup.find("div", attrs={"class": "character-movie"})
        a_tags = div_tags.find_all("a")
        return [tag.get("href") for tag in a_tags]

    def crawler(self, url):
        page_anime_links = list()
        page = 1
        crawl = True
        while page < 3:
            response = self.get_page(url, page)
            if response is not None:
                links = self.find_links(response.text)
                page_anime_links.extend(links)
                print(links)
                page += 1
            else:
                crawl = False
        return page_anime_links

    def start(self):
        switch = sys.argv[1]
        anime_links = list()
        if switch == "find_links":
            for genre, genre_id in self.genre.items():
                print(genre)
                link = self.url(genre_id)
                anime_links.extend(self.crawler(link))
        return anime_links


def store(self):
    pass


class DataCrawler(CrawlerBase):
    def start(self):
        pass

    def store(self):
        pass
