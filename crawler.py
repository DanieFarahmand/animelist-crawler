from concurrent.futures import ThreadPoolExecutor
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from config import STORAGE_TYPE
from parser import AnimeDetailParser
from storage import FileStorage, MongoStorage
from user_info import EMAIL, PASSWORD, URL


class CrawlerBase(ABC):
    """
    The abstract base class for web crawlers. It defines the methods that must be
    implemented by any subclass.
    """

    def __init__(self):
        self.storage = self.__set_storage()  # Create an instance of the storage class.

    @staticmethod
    def __set_storage():
        """
        Set the storage type based on the STORAGE_TYPE variable.
        """
        if STORAGE_TYPE == "mongo":
            return MongoStorage()
        return FileStorage()

    @abstractmethod
    def start(self):
        """
        This method starts the crawling process.
        """
        pass

    @abstractmethod
    def store(self, data, file_name):
        """
        This method stores the data in a file.
        """
        pass


class LinkCrawler(CrawlerBase):
    """
    A subclass of CrawlerBase that crawls the link of anime pages.
    """

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
        """
        This method extracts links to anime shows from the given HTML document.
        """
        soup = BeautifulSoup(html_doc, "html.parser")
        div_tags = soup.find("div", attrs={"class": "character-movie"})
        a_tags = div_tags.find_all("a")
        return [tag.get("href") for tag in a_tags]

    def crawler(self, url):
        """
        This method crawls a page for links to anime pagees.
        """
        page_anime_links = list()
        page = 1
        while page < 3:  # Crawl only 2 pages (replace it with 'self.crawl' to crawl all the pages).
            response = self.get(url + str(page))
            if response is not None:
                links = self.find_links(response.text)
                page_anime_links.extend(links)
                page += 1
            else:
                self.crawl = False  # Stop crawling if all pages crawled.
        return page_anime_links

    def start(self):
        """
        This method starts the crawling process and returns a list of links to anime shows.
        """
        anime_links = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for genre, genre_id in self.genre.items():
                link = self.url(genre_id)
                future = executor.submit(self.crawler, link)
                futures.append(future)
            for future in futures:
                anime_links.extend(future.result())
                self.store([{'url': link, "flag": False} for link in anime_links])
        return anime_links

    def store(self, data, file_name="links"):
        self.storage.store(data, "anime_links", file_name)


class DataCrawler(CrawlerBase):
    """
    A subclass of CrawlerBase that crawls the datas from the links crawled in LinkCrawler.
    """

    def __init__(self):
        super().__init__()
        self.links = self.__load_links()  # load links to crawl
        self.parser = AnimeDetailParser()  # initialize parser object to parse anime details
        self.session = self.login()

    @staticmethod
    def login():
        session = requests.Session()
        response = session.get(URL)
        content = BeautifulSoup(response.text, "html.parser")
        data = {}
        for form in content.find_all("form"):
            for inp in form.select("input[type=hidden]"):
                data[inp.get("name")] = inp.get("value")
        data.update({"email": EMAIL, "password": PASSWORD})
        headers = {"User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"}
        re = session.post(URL, headers=headers, data=data)
        return session

    def get(self, url):
        try:
            response = self.session.get(url)
        except requests.RequestException:
            return None
        return response

    def __load_links(self):
        """
        Load links to crawl from storage.
        """
        return self.storage.load(collection_name="anime_links", filter_data={"flag": False})

    def start(self):
        """
        Crawl and parse anime data for each link, and store the data in storage.
        Update the flag of each link in storage once the data is crawled and stored.
        """
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for link in self.links:
                future = executor.submit(self.__process_link, link)
                futures.append(future)
            for future in futures:
                future.result()

    def __process_link(self, link):
        response = self.get(link["url"])  # send GET request to link
        datas = self.parser.parser(response.text)  # parse anime data
        self.store(anime_data=datas, file_name=datas["title"].replace(" ", "-"))  # store anime data
        self.storage.update_flag(link)  # update flag of the link

    def store(self, anime_data, file_name):
        """
        Store anime data in storage with the given file name.
        """
        self.storage.store(anime_data, "anime_data", file_name)


class ImageDownloader(CrawlerBase):
    """
    A subclass of CrawlerBase that downloads the images from each page that crawled in DataCrawler class.
    """

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
        return self.storage.load("anime_data")  # loads the images url

    def start(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            threads = []
            for anime in self.animes:
                thread = executor.submit(self.download_image, anime)
                threads.append(thread)
            for thread in threads:
                thread.result()

    def download_image(self, anime):
        response = self.get(anime["image"]["url"])  # downloads the image
        self.store(response, file_name=anime['_id'])  # stores the image

    def store(self, data, file_name):
        return self.save_to_disk(data, file_name)

    @staticmethod
    def save_to_disk(response, file_name):
        with open(f"data/images/{file_name}.jpg", "ab") as f:
            f.write(response.content)
            # Save the image to disk with the anime ID as the file name
            print(file_name)
