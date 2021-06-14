from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.http import SessionRequest
import scrapy
from scrapy_playwright.page import PageCoroutine



class BibliRennesSpider(scrapy.Spider):
    name = "bibliRennes"

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
        divs = response.css(".patFunc")
        if len(divs) == 1:
            self.logger.info("Successfully logged to BibliRennes with card " + self.cardId)
            entries = response.css(".patFuncEntries")
            self.parse_entries(entries)

    def parse_entries(self, entries):
        pass

    def parse_details_response(self, response):
        pass
