from functools import partial
from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.items import BookItem, LoanItem
from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.item_loaders import BookLoader, LoanItemLoader
import pytest
from datetime import date
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from hamcrest.library.object.hasproperty import has_property

@pytest.fixture
def book_loader():
    return BookLoader(item=BookItem())


@pytest.fixture
def loan_loader():
    return LoanItemLoader(item=LoanItem())


@pytest.fixture
def item():
    def perform(loader, property_name, value, expected):
        if type(value) == list:
            for val in value:
                loader.add_value(property_name, val)
        else:
            loader.add_value(property_name, value)
        item = loader.load_item()
        assert_that(item, has_property(property_name, equal_to(expected)))
    return perform


@pytest.fixture
def book_item(item, book_loader):
    return partial(item, book_loader)


@pytest.fixture
def loan_item(item, loan_loader):
    return partial(item, loan_loader)


def test_book_loader_title1(book_item):
    book_item("title", 
         "L'imagerie français-arabe / conception et texte Emilie Beaumont",
         "L'imagerie français-arabe")


def test_book_loader_title2(book_item):
    book_item("title",
         " 	Apprendre l'anglais en chantant [Texte imprimé] / orchestrations Lucas Sanner, Renan Napoli ; interprètes Sarah Tullamore et Yann Marshall ; illustrations et conception graphique Adeline Ruel",
         "Apprendre l'anglais en chantant")


def test_book_loader_title3(book_item):
    book_item("title",
         " 	Bienvenue au club ! écrit par Gwenaëlle Boulet ; illustré par Vincent Caut",
         "Bienvenue au club !")


def test_book_loader_title4(book_item):
    book_item("title",
         "A la folie ! [Texte imprimé] / Zep",
         "A la folie !")


def test_book_loader_title5(book_item):
    book_item("title",
         " 	Apprendre l'anglais en chantant Texte imprimé / orchestrations Lucas Sanner, Renan Napoli ; interprètes Sarah Tullamore et Yann Marshall ; illustrations et conception graphique Adeline Ruel",
         "Apprendre l'anglais en chantant")


def test_book_item_notes(book_item):
    book_item("notes", 
        ["notes 1", "notes 2", "notes 3"],
        "notes 1, notes 2, notes 3"
    )


def test_loan_loader_deadline(loan_item):
    loan_item("deadline", "\n   RETOUR 06-07-21         \n", date(2021,7,6))


def test_loan_loader_renewed(loan_item):
    loan_item("renewed", True, True)


def test_loan_loader_status(loan_item):
    loan_item("status", "\n\t   RETOUR 06-07-21         \n", "RETOUR 06-07-21")