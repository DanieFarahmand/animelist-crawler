from crawler import LinkCrawler, DataCrawler, ImageDownloader
from config import genres, crawl_link
import sys

if __name__ == '__main__':
    switch = sys.argv[1]
    if switch == "find_links":
        link_crawler = LinkCrawler(genre=genres, url=crawl_link)
        link_crawler.start()
    elif switch == "extract_links":
        data_crawler = DataCrawler()
        data_crawler.start()
    elif switch == "download_images":
        data_crawler = ImageDownloader()
        data_crawler.start()
