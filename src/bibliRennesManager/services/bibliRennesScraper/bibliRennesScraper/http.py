from scrapy.http.request import Request

class SessionRequest(Request):
    def __init__(self, sessionId=None, *args, **kwargs):
        self.sessionId = sessionId
        super().__init__(
            dont_filter=True, 
            meta={"playwright": True, "playwright_include_page": True}, 
            *args, **kwargs)
