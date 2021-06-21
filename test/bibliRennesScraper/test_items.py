from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.items import BookItem, BookLoader

def test_book_loader_title():
    titles = [
        {
            "value": "L'imagerie français-arabe / conception et texte Emilie Beaumont",
            "expected": "L'imagerie français-arabe"
        },
        {
            "value": " 	Apprendre l'anglais en chantant [Texte imprimé] / orchestrations Lucas Sanner, Renan Napoli ; interprètes Sarah Tullamore et Yann Marshall ; illustrations et conception graphique Adeline Ruel",
            "expected": "Apprendre l'anglais en chantant"
        },
        {
            "value": " 	Bienvenue au club ! écrit par Gwenaëlle Boulet ; illustré par Vincent Caut",
            "expected": "Bienvenue au club !"
        },
        {
            "value": "A la folie ! [Texte imprimé] / Zep",
            "expected": "A la folie !"
                        ""
        }
    ]

    for current_title in titles:
        loader = BookLoader(item=BookItem())

        loader.add_value("title", current_title["value"])
        item = loader.load_item()
        assert item.title == current_title["expected"]
