from .items import Exemplaire
from scrapy.utils.deprecate import create_deprecated_class
from datetime import datetime


def extract_title(title: str):
    if "[" in title:
        return title.split("[")[0]
    elif "Texte" in title:
        return title[:title.index("Texte")]
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

class ToDict:
    def __call__(self, values):
        return {k:v for (k,v) in values}



