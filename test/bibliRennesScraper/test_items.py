import hamcrest
from hamcrest.library.object.hasproperty import has_property
from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.items import BookItem, BookLoader
import pytest
from datetime import date
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to

@pytest.fixture
def loader():
    return BookLoader(item=BookItem())


@pytest.fixture
def item(loader):
    def perform(property_name, value, expected):
        loader.add_value(property_name, value)
        item = loader.load_item()
        assert_that(item, has_property(property_name, equal_to(expected)))
    return perform



def test_book_loader_title1(item):
    item("title", 
         "L'imagerie français-arabe / conception et texte Emilie Beaumont",
         "L'imagerie français-arabe")


def test_book_loader_title2(item):
    item("title",
         " 	Apprendre l'anglais en chantant [Texte imprimé] / orchestrations Lucas Sanner, Renan Napoli ; interprètes Sarah Tullamore et Yann Marshall ; illustrations et conception graphique Adeline Ruel",
         "Apprendre l'anglais en chantant")


def test_book_loader_title3(item):
    item("title",
         " 	Bienvenue au club ! écrit par Gwenaëlle Boulet ; illustré par Vincent Caut",
         "Bienvenue au club !")


def test_book_loader_title4(item):
    item("title",
         "A la folie ! [Texte imprimé] / Zep",
         "A la folie !")


def test_book_loader_deadline(item):
    item("deadline", "\n   RETOUR 06-07-21         \n", date(2021,7,6))


def test_book_loader_renewed(item):
    item("renewed", True, True)