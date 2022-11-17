from src.bibliRennesManager.services.bibliRennesScraper.test.utils import fake_response_from_file
from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.spiders.account_spider import BibliRennesAccountSpider
from scrapy.http import Response
from hamcrest.core import assert_that
from hamcrest.library.object.haslength import has_length
from hamcrest.library.collection.issequence_containing import has_items
from hamcrest.library.object.hasproperty import has_properties, has_property
from hamcrest.core.core.isequal import equal_to
import pytest


@pytest.fixture
def account_response():
    response = fake_response_from_file("compte_lecteur_items.html")
    parent_response = Response(url=response.url)
    parent_response.frames = {"accountContentIframe": response}
    return parent_response


@pytest.fixture
def spider():
    return BibliRennesAccountSpider("123456789", "password1")


def test_spider_account(account_response, spider):
    result = spider.parse_login_response(account_response)
    requests = list(result)
    def get_item(x):
        return x.meta["data"]
    items = list(map(get_item, requests))
    
    assert_that(requests, has_length(32))
    assert_that(requests, has_items(
        has_property("url", equal_to("https://opac.si.leschampslibres.fr/iii/encore/record/C__Rb1060092?lang=frf&suite=def")),
        has_property("url", equal_to("https://opac.si.leschampslibres.fr/iii/encore/record/C__Rb1843465?lang=frf&suite=def"))
    ))
    assert_that(items, has_items(
        has_properties({"barcode": "33500600918569",
                        "cote": "P 840",
                        "status": "RETOUR 06-07-21",
                        "renewed": True
                        }),
        has_properties({"barcode": "33500600861371",
                        "cote": "BD L",
                        "status": "RETOUR 06-07-21",
                        "renewed": True
                        }),
        has_properties({"barcode": "33500600912059",
                        "cote": "RE VAL",
                        "status": "RETOUR 06-07-21",
                        "renewed": False
                        })
    ))