from scrapy.http import Request
from bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.http import SessionRequest
from scrapy.crawler import CrawlerProcess
import scrapy

# class ServerError(Error):
#
#     def __init__(self, serverUrl, message):
#         self.serverUrl = serverUrl
#         self.message = message


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
        req = SessionRequest(url=self.login_url, 
                        callback=self.parse_login_response,
                        sessionId=self.cardId)
        yield req


    def parse_login_response(self, response):
        page = response.meta["playwright_page"]
        page.fill("input#code", self.cardId)
        page.fill("input#pin", self.cardPassword)
        page.click('//input[@name="submit"]')
        
        yield scrapy.Request(self.account_url, callback=self.parse_account, dont_filter=True,)
        
    def parse_account(self, response):
        if response.status != 200:
            raise NameError("Server connection exeption")


    def parse_account_response(self, response):
        pass

    def parse_details_response(self, response):
        pass



