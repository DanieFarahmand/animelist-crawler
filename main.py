from crawler import LinkCrawler
from config import genres, crawl_link

if __name__ == '__main__':
    link_crawler = LinkCrawler(genre=genres, url=crawl_link)
    link_crawler.start()
