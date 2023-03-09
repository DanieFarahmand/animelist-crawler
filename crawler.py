from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

from config import STORAGE_TYPE
from parser import AnimeDetailParser
from storage import FileStorage, MongoStorage
from login import Browser


class CrawlerBase(ABC):

    def __init__(self):
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == "mongo":
            return MongoStorage()
        return FileStorage()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data, file_name):
        pass

    @abstractmethod
    def get(self, url):
        pass


class LinkCrawler(CrawlerBase):
    def __init__(self, genre, url):
        self.genre = genre
        self.url = url
        self.crawl = True
        super().__init__()

    def get(self, url):
        try:
            response = requests.get(url)
        except requests.RequestException:
            return None
        return response

    @staticmethod
    def find_links(html_doc):
        soup = BeautifulSoup(html_doc, "html.parser")
        div_tags = soup.find("div", attrs={"class": "character-movie"})
        a_tags = div_tags.find_all("a")
        return [tag.get("href") for tag in a_tags]

    def crawler(self, url):
        page_anime_links = list()
        page = 1
        while page < 3:
            response = self.get(url + str(page))
            if response is not None:
                links = self.find_links(response.text)
                page_anime_links.extend(links)
                page += 1
            else:
                self.crawl = False
        return page_anime_links

    def start(self):
        anime_links = list()
        for genre, genre_id in self.genre.items():
            link = self.url(genre_id)
            anime_links.extend(self.crawler(link))
            self.store([{'url': link, "flag": False} for link in anime_links])
        return anime_links

    def store(self, data, file_name="links"):
        self.storage.store(data, "anime_links", file_name)


class DataCrawler(CrawlerBase):

    def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.parser = AnimeDetailParser()

    def get(self, url):
        cookie = Browser()
        try:
            response = requests.get(url, cookies=cookie.login(url))
        except requests.RequestException:
            return None
        return response

    def __load_links(self):
        return self.storage.load(collection_name="anime_links", filter_data={"flag": False})

    def start(self):
        for link in self.links:
            response = self.get(link["url"])
            datas = self.parser.parser(response.text)
            self.store(anime_data=datas, file_name=datas["title"].replace(" ", "-"))
            self.storage.update_flag(link)

    def store(self, anime_data, file_name):
        self.storage.store(anime_data, "anime_data", file_name)


class ImageDownloader(CrawlerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animes = self.__image_loader()

    @staticmethod
    def get(url):
        try:
            response = requests.get(url, stream=True)
        except requests.RequestException:
            return None
        return response

    def __image_loader(self):
        return self.storage.load("anime_data")

    def start(self):
        for anime in self.animes:
            print(anime)
            response = self.get(anime["image"]["url"])
            self.store(response, file_name=anime['_id'])

    def store(self, data, file_name):
        return self.save_to_disk(data, file_name)

    @staticmethod
    def save_to_disk(response, file_name):
        with open(f"data/images/{file_name}.jpg", "ab") as f:
            f.write(response.content)
            print(file_name)
