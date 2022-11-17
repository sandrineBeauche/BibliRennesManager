from scrapy.http.request import Request


class SessionRequest(Request):
    def __init__(self, sessionId=None, page_methods=None, password=None, *args, **kwargs):
        self.sessionId = sessionId
        self.password = password
        meta_dict = {"playwright": True, "playwright_include_page": True}
        if page_methods is not None:
            meta_dict["playwright_page_methods"] = page_methods
        super().__init__(
            dont_filter=True, 
            meta=meta_dict,
            *args, **kwargs)
