from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.http import SessionRequest
from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.items import BookItem
import scrapy
from scrapy_playwright.page import PageCoroutine
from scrapy.loader import ItemLoader


class BibliRennesSpider(scrapy.Spider):
    name = "bibliRennes"

    account_url = "https://opac.si.leschampslibres.fr/iii/encore/myaccount"

    cardId = None
    cardPassword = None

    bookLoaders = {}

    def __init__(self, cardId=None, cardPassword=None, *args, **kwargs):
        super(BibliRennesSpider, self).__init__(*args, **kwargs)
        self.cardId = cardId
        self.cardPassword = cardPassword

    def start_requests(self):
        page_coro = [
            PageCoroutine("fill", selector="input#code", value=self.cardId),
            PageCoroutine("fill", selector="input#pin", value=self.cardPassword),
            PageCoroutine("click", selector='//input[@name="submit"]'),
        ]
        req = SessionRequest(url=self.account_url,
                             callback=self.parse_login_response,
                             sessionId=self.cardId,
                             page_coro=page_coro)
        yield req

    def parse_login_response(self, response):
        if not hasattr(response, "frames"):
            self.logger.error("Failed to login with id " + self.cardId)
        else:
            self.logger.info("Successfully logged to BibliRennes with card " + self.cardId)
            elts = response.frames["accountContentIframe"].css("tr.patFuncEntry")
            requests = self.parse_entries(elts)
            for req in requests:
                yield req

    def parse_entries(self, entries):
        result = []
        for current_entry in entries:
            loader = ItemLoader(item=BookItem(), selector=current_entry)
            barcode = current_entry.xpath("td[@class='patFuncBarcode']/text()").get()
            loader.add_value("barcode", barcode)
            loader.add_xpath("cote", "td[@class='patFuncCallNo']/text()")
            loader.add_xpath("status", "td[@class='patFuncStatus']/text()")
            self.bookLoaders[barcode] = loader
            url = current_entry.xpath("th/a/@href").get()
            req = SessionRequest(url=url,
                                 callback=self.parse_details_response,
                                 sessionId=self.cardId)
            req.meta["barcode"] = barcode
            result.append(req)
        return result

    def parse_details_response(self, response):
        barcode = response.meta["barcode"]
        loader = self.bookLoaders[barcode]
        loader.add_xpath("title", "//div[@id='bibTitle']/text()")
        loader.add_xpath("authors", "//div[@id='dpBibAuthor']/a/text()")
        item = loader.load_item()
        return item