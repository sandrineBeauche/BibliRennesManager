import os

from scrapy.http import HtmlResponse, Request
from scrapy.selector.unified import Selector


def get_file_content(file_name):
    if not file_name[0] == '/':
        responses_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(responses_dir, file_name)
    else:
        file_path = file_name

    file_content = open(file_path, 'r').read()
    return file_content


def selector_from_file(file_name, expr):
    file_content = get_file_content(file_name)
    sel = Selector(text=file_content)
    result = sel.xpath(expr)[0]
    return result


def fake_response_from_file(file_name, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = 'http://www.example.com'

    request = Request(url=url)

    file_content = get_file_content(file_name)
    response = HtmlResponse(url=url,
                        request=request,
                        body=file_content,
                        encoding='utf-8')
    return response
