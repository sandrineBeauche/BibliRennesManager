# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import date


@dataclass
class Exemplaire:
    localisation: Optional[str] = field(default=None)
    cote: Optional[str] = field(default=None)
    status: Optional[str] = field(default=None)
    condition: Optional[str] = field(default=None)


@dataclass
class BookItem:
    title: Optional[str] = field(default=None)
    authors: Optional[str] = field(default=None)
    exemplaires: List[Exemplaire] = field(default_factory=list)
    url: Optional[str] = field(default=None)
    notes: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    publication: Optional[str] = field(default=None)
    resume: Optional[str] = field(default=None)
    cover: Optional[str] = field(default=None)
    
    

@dataclass
class LoanItem:
    book: Optional[BookItem] = field(default=BookItem())
    barcode: Optional[str] = field(default=None)
    cote: Optional[str] = field(default=None)
    library: Optional[str] = field(default=None)
    deadline: Optional[date] = field(default=None)
    reservation: Optional[bool] = field(default=False)
    renewed: Optional[bool] = field(default=False)
    status: Optional[str] = field(default=None)
    cardId: Optional[str] = field(default=None)
    #image_urls: List[str] = field(default_factory=list)
    #images: List = field(default_factory=list)
