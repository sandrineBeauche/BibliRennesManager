from ..items import BookItem, Exemplaire
from ..item_loaders import ExemplaireLoader, BookLoader
import scrapy


class BibliRennesSpider(scrapy.Spider):




    def parse_details_response(self, response):
        def parse_exemplar(current_exemplar):
            exemplar_loader = ExemplaireLoader(item=Exemplaire(), selector=current_exemplar)
            exemplar_loader.add_xpath("localisation", "td[1]/a/text()")
            exemplar_loader.add_xpath("cote", "td[2]/span/a/text()")
            exemplar_loader.add_xpath("status", "td[3]/text()")
            exemplar_loader.add_xpath("condition", "td[4]/text()")
            return exemplar_loader.load_item()

        exemplars = [parse_exemplar(current)
                     for current in response.xpath("//table[@class='itemTable']/tr")[1:]]
        book_loader = BookLoader(item=BookItem())
        book_loader.add_xpath("authors", "//div[@id='dpBibAuthor']/a/text()")
        book_loader.add_value("exemplaires", exemplars)
        return book_loader.load_item()
