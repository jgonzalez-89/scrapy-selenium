import datetime

# Obtén la fecha actual
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Concatena la fecha con la extensión del archivo de salida
output_file = f"{current_date}.json"

BOT_NAME = "selenium_amazon"

SPIDER_MODULES = ["selenium_amazon.spiders"]
NEWSPIDER_MODULE = "selenium_amazon.spiders"

ITEM_PIPELINES = {
    'selenium_amazon.pipelines.TransformDataPipeline': 300,
}


# Configuración del archivo de salida
FEED_FORMAT = 'json'
FEED_URI = output_file


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
SELENIUM_DRIVER_EXECUTABLE_PATH = "geckodriver.exe"
SELENIUM_DRIVER_ARGUMENTS = ['-headless']

DOWNLOAD_DELAY = 5
