# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass, field
from typing import Optional
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose
from scrapy.loader import ItemLoader



@dataclass
class BookItem:
    # define the fields for your item here like:
    barcode: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    authors: Optional[str] = field(default=None)
    cote: Optional[str] = field(default=None)
    status: Optional[str] = field(default=None)


class BookLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    title_in = Compose(lambda v: v.strip(' '))