from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.http import SessionRequest
import scrapy
from scrapy_playwright.page import PageCoroutine



class BibliRennesSpider(scrapy.Spider):
    name = "bibliRennes"

    login_url = "https://sbib.si.leschampslibres.fr/iii/cas/login"

    account_url = "https://opac.si.leschampslibres.fr/iii/encore/myaccount?lang=frf"

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
            PageCoroutine("wait_for_load_state")
        ]
        req = SessionRequest(url=self.login_url,
                             callback=self.parse_login_response,
                             sessionId=self.cardId,
                             page_coro=page_coro)
        yield req

    def parse_login_response(self, response):
        divs = response.css(".success")
        if len(divs) == 1:
            self.logger.info("Successfully logged to BibliRennes with card " + self.cardId)
            yield SessionRequest(url=self.account_url,
                                 callback=self.parse_account,
                                 sessionId=self.cardId)

    def parse_account(self, response):
        if response.status != 200:
            raise NameError("Server connection exeption")

    def parse_account_response(self, response):
        pass

    def parse_details_response(self, response):
        pass
