import time
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from webdriver_manager.firefox import GeckoDriverManager

class SeleniumMiddleware:
    def __init__(self):
        # Obtiene las configuraciones del proyecto
        settings = get_project_settings()

        # Configura las opciones del navegador
        options = Options()
        for argument in settings.get("SELENIUM_DRIVER_ARGUMENTS"):
            options.add_argument(argument)

        self.driver = Firefox(executable_path=GeckoDriverManager().install(), options=options)


    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(2)  # pausa de 2 segundos
        return HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)

