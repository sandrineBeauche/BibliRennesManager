from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def launch():
    process = CrawlerProcess(get_project_settings())
    process.crawl("bibliRennes")
    process.start()


if __name__ == '__main__':
    launch()
