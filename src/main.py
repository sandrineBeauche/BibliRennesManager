from bibliRennesManager.services.bibliRennesScraper.bibliRennesScraperLauncher import launch
import json
from os.path import exists
import os
from datetime import datetime as dt
import logging


ITEMS_FILE_PATH = "bibliRennesManager/services/bibliRennesScraper/items.json"

def launch_scraping():
    with open('cards.json') as json_file:
        cards = json.load(json_file)
        launch(cards)

def check_file_items():
    if exists(ITEMS_FILE_PATH):
        file_time_string = dt.fromtimestamp(os.path.getmtime(__file__))
        d = file_time_string.date()
        today = dt.today().date()
        if d < today:
            logging.info("items.json is outdated. Removing and scraping again...")
            os.remove(ITEMS_FILE_PATH)
            return False
        else:
            logging.info("items.json is up-to-date.")
            return True
    else:
        logging.info("items.json is not yet scraped. Begin scraping...")
        return False


def process():
    logging.basicConfig(level=logging.INFO)
    if not check_file_items():
        launch_scraping()

if __name__ == '__main__':
    process()


