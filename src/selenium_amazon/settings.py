BOT_NAME = "selenium_amazon"

SPIDER_MODULES = ["selenium_amazon.spiders"]
NEWSPIDER_MODULE = "selenium_amazon.spiders"

ROBOTSTXT_OBEY = True


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOADER_MIDDLEWARES = {
    'selenium_amazon.middlewares.SeleniumMiddleware': 800,
}


SELENIUM_DRIVER_NAME = "firefox"
SELENIUM_DRIVER_EXECUTABLE_PATH = "C:\\Users\\Jose L\\Downloads\\geckodriver.exe"
SELENIUM_DRIVER_ARGUMENTS = []

DOWNLOAD_DELAY = 5
