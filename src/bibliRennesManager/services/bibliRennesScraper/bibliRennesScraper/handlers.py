from playwright.async_api import Page
from scrapy_playwright.handler import ScrapyPlaywrightDownloadHandler
from src.bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.http import SessionRequest


class BibliRennesmanagerDownloadHandler(ScrapyPlaywrightDownloadHandler):

    async def login(self, request: SessionRequest) -> Page:
        page = await self._create_page(request)
        await page.goto(url="https://opac.si.leschampslibres.fr/iii/encore/myaccount?lang=frf")
        await page.locator("input[name=\"code\"]").fill(request.sessionId)
        await page.locator("input[name=\"pin\"]").fill(request.password)
        await page.locator("input[name=\"submit\"]").click()
        return page
