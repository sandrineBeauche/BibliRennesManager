# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime

import scrapy
from dataclasses import dataclass, field
from typing import Optional
from itemloaders.processors import Identity, TakeFirst, MapCompose, Join, Compose
from scrapy.loader import ItemLoader
from scrapy.utils.deprecate import create_deprecated_class


@dataclass
class BookItem:
    # define the fields for your item here like:
    barcode: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    authors: Optional[str] = field(default=None)
    cote: Optional[str] = field(default=None)
    status: Optional[str] = field(default=None)
    library: Optional[str] = field(default=None)
    deadline: Optional[datetime] = field(default=None)
    reservation: Optional[bool] = field(default=False)
    renewed: Optional[bool] = field(default=False)


def extract_title(title: str):
    if "[" in title:
        return title.split("[")[0]
    elif "/" in title:
        return title.split("/")[0]
    elif "!" in title:
        return title[:title.index("!") + 1]
    elif "?" in title:
        return title[:title.index("?") + 1]
    else:
        return title


def extract_author(author: str):
    if "(" in author:
        return author.split("(")[0]
    else:
        return author

def stripAll(value: str): 
    return value.strip("\n\t ")


def extract_deadline(value: str):
    return datetime.strptime(value, "RETOUR %d-%m-%y").date()


class BooleanOr:
    def __call__(self, values):
        return any(values)

BooleanOrProc = create_deprecated_class("BooleanOr", BooleanOr)


class BookLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    title_in = MapCompose(extract_title, str.strip)
    
    authors_in = MapCompose(extract_author, str.strip)
    authors_out = Join(separator=',')

    status_in = MapCompose(stripAll)

    deadline_in = MapCompose(str.strip, extract_deadline)
    renewed_in = Identity()
    renewed_out = BooleanOrProc()
    reservation_in = Identity()
    reservation_out = BooleanOrProc()