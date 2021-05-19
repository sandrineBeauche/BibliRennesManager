from scrapy.http import FormRequest
from scrapy.crawler import CrawlerProcess
import scrapy

# class ServerError(Error):
#
#     def __init__(self, serverUrl, message):
#         self.serverUrl = serverUrl
#         self.message = message


class BibliRennesSpider(scrapy.Spider):
    name = "bibliRennes"

    login_url = "https://sbib.si.leschampslibres.fr/iii/cas/login?service=https%3A%2F%2Fopac.si.leschampslibres.fr%3A443%2Fiii%2Fencore%2Fj_acegi_cas_security_check&lang=frf&suite=pearl"

    account_url = "https://opac.si.leschampslibres.fr/iii/encore/myaccount?lang=frf"

    def start_requests(self):
        yield FormRequest(self.login_url,
                          formdata={"code": "23500002705434",
                                    "pin": "9ewxxjIUAfLcYGIKY1CT"},
                          callback=self.parse_login_response)


    def parse_login_response(self, response):
        if response.status == 200:
            yield scrapy.Request(self.account_url, callback=self.parse_account, dont_filter=True)
        else:
            raise NameError("Server connection exeption")

    def parse_account(self, response):
        if response.status != 200:
            raise NameError("Server connection exeption")


    def parse_account_response(self, response):
        pass

    def parse_details_response(self, response):
        pass



