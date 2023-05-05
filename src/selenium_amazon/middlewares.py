import time
from scrapy.http import HtmlResponse
from selenium.webdriver import Firefox
from webdriver_manager.firefox import GeckoDriverManager

class SeleniumMiddleware:
    def __init__(self):
        self.driver = Firefox(executable_path=GeckoDriverManager().install())

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(2)  # pausa de 2 segundos
        return HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)

