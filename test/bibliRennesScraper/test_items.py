from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.items import BookItem, BookLoader

def test_book_loader_title():
    loader = BookLoader(item=BookItem())
    value = '\n                   \n                       Au creux de mon arbre Texte imprimé [Patricia Hegarty] ' \
            'illustré par Britta Teckentrup [traduction française et adaptation, Frédéric Rébéna]\n                   ' \
            '\n                   \n                   \n '
    expected = "Au creux de mon arbre"
    loader.add_value("title", value)
    item = loader.load_item()
    assert item.title == expected
