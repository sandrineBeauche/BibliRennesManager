from scrapy.http.request import Request

class SessionRequest(Request):
    def __init__(self, sessionId=None, page_coro=None, *args, **kwargs):
        self.sessionId = sessionId
        meta_dict = {"playwright": True, "playwright_include_page": True}
        if page_coro is not None:
            meta_dict["playwright_page_coroutines"] = page_coro
        super().__init__(
            dont_filter=True, 
            meta=meta_dict,
            *args, **kwargs)
