from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.spiders.bibliRennesSpider import BibliRennesSpider, parse_exemplar
import pytest
from .utils import fake_response_from_file, selector_from_file
from hamcrest.core import assert_that
from hamcrest.library.object.hasproperty import has_properties, has_property
from hamcrest.library.object.haslength import has_length
from hamcrest.core.core.isnone import none
from scrapy.selector import Selector

@pytest.fixture
def livre1_response():
    return fake_response_from_file("livre1.html")

@pytest.fixture
def livre2_response():
    return fake_response_from_file("livre2.html")


@pytest.fixture
def spider():
    return BibliRennesSpider()


@pytest.fixture
def exemplar1():
    return selector_from_file("exemplar1.html", "//html/body/table/tr")

@pytest.fixture
def exemplar2():
    return selector_from_file("exemplar2.html", "//html/body/table/tr")


def test_parse_exemplar1(exemplar1):
    result = parse_exemplar(exemplar1)
    assert_that(result, has_properties({
        "localisation": "Champs-Manceaux enfant",
        "cote": "BD HER",
        "status": "EN RAYON",
        "condition": "."
    }))



def test_spider_book1(livre1_response, spider):
    result = spider.parse_details_response(livre1_response)
    assert_that(result, has_properties({
        "title": "L'héritage de Rantanplan",
        "authors": "Morris - Goscinny, René",
        "exemplaires": has_length(2),
        "notes": "Vol. 41 dans l'ordre chronologique",
        "description": "47 p. ill. en noir et en coul., couv. ill. en coul. 30 cm",
        "publication": "[Givrins] (Suisse) : Lucky comics [Paris] : [diff. Dargaud], 2003 (93-Pantin  : Impr. PPO graphic)",
        "resume": None
    }))


def test_spider_book2(livre2_response, spider):
    result = spider.parse_details_response(livre2_response)
    assert_that(result, has_properties({
        "title": "Ramdam sur le rift",
        "authors": "Herlé - Widenlocher, Roger",
        "exemplaires": has_length(6),
        "notes": '',
        "description": "47p.",
        "publication": "Paris : Dargaud, 1999",
        "resume": None
    }))