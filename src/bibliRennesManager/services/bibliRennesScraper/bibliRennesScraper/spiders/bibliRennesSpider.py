from ..items import BookItem, Exemplaire
from ..item_loaders import ExemplaireLoader, BookLoader
import scrapy



def parse_exemplar(current_exemplar):
    exemplar_loader = ExemplaireLoader(item=Exemplaire(), selector=current_exemplar)
    if current_exemplar.xpath("td[1]/a").get() is not None:
        exemplar_loader.add_xpath("localisation", "td[1]/a/text()")
    else:
        exemplar_loader.add_xpath("localisation", "td[1]/text()")
    exemplar_loader.add_xpath("cote", "td[2]/span/a/text()")
    exemplar_loader.add_xpath("status", "td[3]/text()")
    exemplar_loader.add_xpath("condition", "td[4]/text()")
    return exemplar_loader.load_item()






class BibliRennesSpider(scrapy.Spider):

    name = "bibliRennesBook"

    def parse_details_response(self, response):
        rows = response.xpath("//table[@class='itemTable']/tbody/tr")[1:]
        exemplars = [parse_exemplar(current)
                     for current in rows]
        #selector="//div[@id='mainContentArea']"
        book_loader = BookLoader(item=BookItem(), response=response)
        book_loader.add_xpath("title", "//div[@id='bibTitle']/text()")

        book_loader.add_details_values("AUTEUR(S)", True, "authors")
        book_loader.add_details_values("AUT. SECOND.", True, "authors")
        book_loader.add_details_values("CO-AUTEUR(S)", True, "authors")

        book_loader.add_value("exemplaires", exemplars)
        book_loader.add_value("url", response.url)
        
        book_loader.add_details_values("PUBLICATION", False, "publication")
        book_loader.add_details_values("NOTES", False, "notes")
        book_loader.add_details_values("DESCRIPTION", False, "description")
        book_loader.add_details_values("RESUME", False, "resume")

        book_loader.add_xpath("cover", "//div[@class='itemBookCover']/div/img/@src")
        
        return book_loader.load_item()
