import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from os import getcwd, chdir, path


def launch():
    pwd = getcwd()
    scraper_dir = path.dirname(path.realpath(__file__))
    chdir(scraper_dir)
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl("bibliRennesAccount", "23500002705434", "9ewxxjIUAfLcYGIKY1CT")
    chdir(pwd)
    process.start()


if __name__ == '__main__':
    launch()
