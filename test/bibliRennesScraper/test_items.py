from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.items import BookItem, BookLoader
import pytest


@pytest.fixture
def loader():
    return BookLoader(item=BookItem())


@pytest.fixture
def item(loader):
    def get_item(property_name, value):
        loader.add_value(property_name, value)
        return loader.load_item()
    return get_item


@pytest.fixture
def item_title(item):
    def perform(value, expected):
        it = item("title", value)
        assert it.title == expected
    return perform


def test_book_loader_title1(item_title):
    item_title("L'imagerie français-arabe / conception et texte Emilie Beaumont",
               "L'imagerie français-arabe")


def test_book_loader_title2(item_title):
    item_title(" 	Apprendre l'anglais en chantant [Texte imprimé] / orchestrations Lucas Sanner, Renan Napoli ; interprètes Sarah Tullamore et Yann Marshall ; illustrations et conception graphique Adeline Ruel",
               "Apprendre l'anglais en chantant")


def test_book_loader_title3(item_title):
    item_title(" 	Bienvenue au club ! écrit par Gwenaëlle Boulet ; illustré par Vincent Caut",
               "Bienvenue au club !")


def test_book_loader_title4(item_title):
    item_title("A la folie ! [Texte imprimé] / Zep",
               "A la folie !")