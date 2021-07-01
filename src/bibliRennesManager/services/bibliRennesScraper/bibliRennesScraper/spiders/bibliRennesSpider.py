from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.http import SessionRequest
from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.items import BookItem, BookLoader
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
            return self.parse_entries(elts)
            

    def parse_entries(self, entries):
        for current_entry in entries:
            loader = BookLoader(item=BookItem(), selector=current_entry)
            barcode = current_entry.xpath("td[@class='patFuncBarcode']/text()").get()
            loader.add_value("barcode", barcode)
            loader.add_xpath("cote", "td[@class='patFuncCallNo']/text()")
            loader.add_xpath("status", "td[@class='patFuncStatus']/text()")
            loader.add_xpath("title", "descendant::span[@class='patFuncTitleMain']/text()")
            if len(current_entry.css("span.patFuncRenewCount")) > 0:
                loader.add_value("renewed", True)
            self.bookLoaders[barcode] = loader
            url = current_entry.xpath("th/a/@href").get()
            req = SessionRequest(url=url,
                                 callback=self.parse_details_response,
                                 sessionId=self.cardId)
            req.meta["data"] = loader
            yield req
            

    def parse_details_response(self, response):
        loader = response.meta["data"]
        loader.add_xpath("authors", "//div[@id='dpBibAuthor']/a/text()")
        item = loader.load_item()
        return item