from scrapy.http import FormRequest
from scrapy.crawler import CrawlerProcess
import scrapy
from scrapy_headless import SeleniumRequest

# class ServerError(Error):
#
#     def __init__(self, serverUrl, message):
#         self.serverUrl = serverUrl
#         self.message = message


class BibliRennesSpider(scrapy.Spider):
    name = "bibliRennes"

    login_url = "https://sbib.si.leschampslibres.fr/iii/cas/login"
    account_url = "https://opac.si.leschampslibres.fr/iii/encore/myaccount?lang=frf"
    logout_url = "https://sbib.si.leschampslibres.fr/iii/cas/logout"

    def start_requests(self):
        yield SeleniumRequest(url=self.login_url,
                              callback=self.parse_login)

    def parse_login(self, response):
        driver = response.interact
        eltCode = driver.find_element_by_css_selector("input#code")
        eltCode.send_keys("23500002705434")
        eltPin = driver.find_element_by_css_selector("input#pin")
        eltPin.send_keys("9ewxxjIUAfLcYGIKY1CT")
        response = response.click('//input[@name="submit"]')

        if response.css("div.accountSummary") != []:
            print("coucou")

        self.parse_account(response)

        yield Request(url=self.logout_url)



    def parse_account(self, response):
        if response.status != 200:
            raise NameError("Server connection exeption")





    def parse_details_response(self, response):
        pass



