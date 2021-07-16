from .bibliRennesSpider import BibliRennesSpider
from scrapy_playwright.page import PageCoroutine
from ..http import SessionRequest
from ..items import LoanItem
from ..item_loaders import LoanItemLoader

class BibliRennesAccountSpider(BibliRennesSpider):
    name = "bibliRennesAccount"

    account_url = "https://opac.si.leschampslibres.fr/iii/encore/myaccount"

    cardId = None
    cardPassword = None

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
            loader = LoanItemLoader(item=LoanItem(), selector=current_entry)
            barcode = current_entry.xpath("td[@class='patFuncBarcode']/text()").get()
            loader.add_value("barcode", barcode)
            loader.add_xpath("cote", "td[@class='patFuncCallNo']/text()")
            loader.add_xpath("status", "td[@class='patFuncStatus']/text()")
            if len(current_entry.css("span.patFuncRenewCount")) > 0:
                loader.add_value("renewed", True)
            url = current_entry.xpath("th/a/@href").get()
            req = SessionRequest(url=url,
                                 callback=self.parse_details_response,
                                 sessionId=self.cardId)
            req.meta["data"] = loader.load_item()
            yield req

    def parse_details_response(self, response):
        book =  super().parse_details_response(response)
        result = response.meta["data"]
        result.book = book
        yield result