from ..items import BookItem, Exemplaire
from ..item_loaders import ExemplaireLoader
import scrapy


class BibliRennesSpider(scrapy.Spider):
    
    def parse_details_response(self, response):
        exemp = []
        for current_examplaire in response.xpath("//table[@class='itemTable']/tr")[1:]:
            loader = ExemplaireLoader(item=Exemplaire(), selector=current_examplaire)
            loader.add_xpath("localisation", "td[1]/a/text()")
            loader.add_xpath("cote", "td[2]/span/a/text()")
            loader.add_xpath("status", "td[3]/text()")
            loader.add_xpath("condition", "td[4]/text()")
            exemp.append(loader.load_item())


        
        loader = response.meta["data"]
        loader.add_xpath("authors", "//div[@id='dpBibAuthor']/a/text()")
        item = loader.load_item()
        return {"exemplaires": exemp}
