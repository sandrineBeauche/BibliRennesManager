# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.responsetypes import responsetypes

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from bibliRennesManager.services.bibliRennesScraper.bibliRennesScraper.http import SessionRequest


class BiblirennesscraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SessionPlaywrightDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    crawlerObject = None

    contexts = {}

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        s.crawlerObject = crawler
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    async def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if isinstance(request, SessionRequest):
            sessionId = request.sessionId
            page = await self.create_page(sessionId)
            request.meta["playwright_page"] = page

        return None


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        if exception.name == "TimeoutError" and "waiting for selector" in exception.message:
            request.meta["playwright_page_coroutines"] = []
            return request
        else:
            pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    async def create_page(self, sessionId):
        if(sessionId in self.contexts):
            current_context = self.contexts[sessionId]
        else:
            handlers = self.crawlerObject.engine.downloader.handlers
            pwHandler = handlers._handlers["http"]
            browser = pwHandler.browser
            current_context = await browser.new_context(**pwHandler.context_args)
            self.contexts[sessionId] = current_context
        page = await current_context.new_page() 
        return page


class PlaywrightFrameDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None


    async def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        if "playwright_page" not in response.meta:
            return response
        page = response.meta["playwright_page"]
        if len(page.frames) < 2:
            return response

        response.frames = {}
        for current_frame in page.frames:
            body = (await current_frame.content()).encode("utf8")
            resp_cls = responsetypes.from_args(headers=response.headers, url=current_frame.url, body=body)
            sub_response = resp_cls(url=current_frame.url,
                                    status=response.status,
                                    headers=response.headers,
                                    body=body,
                                    request=request
                                    )
            response.frames[current_frame.name] = sub_response

        return response



    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)