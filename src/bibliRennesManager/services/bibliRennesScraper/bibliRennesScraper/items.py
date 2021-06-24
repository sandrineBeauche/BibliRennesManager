# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime

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
    library: Optional[str] = field(default=None)
    deadline: Optional[datetime] = field(default=None)
    reservation: Optional[bool] = field(default=False)




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




class BookLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    title_in = MapCompose(extract_title, str.strip)