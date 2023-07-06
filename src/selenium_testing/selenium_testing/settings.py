# Scrapy settings for selenium_testing project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import datetime


# Obtén la fecha actual
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Concatena la fecha con la extensión del archivo de salida
output_file = f"{current_date}.json"

BOT_NAME = "selenium_testing"

SPIDER_MODULES = ["selenium_testing.spiders"]
NEWSPIDER_MODULE = "selenium_testing.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "selenium_testing.pipelines.TransformDataPipeline": 300,
}


# Configuración del archivo de salida
FEED_FORMAT = "json"
FEED_URI = output_file

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "selenium_google (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOADER_MIDDLEWARES = {
    "selenium_testing.middlewares.SeleniumMiddleware": 800,
}


SELENIUM_DRIVER_NAME = "firefox"
SELENIUM_DRIVER_EXECUTABLE_PATH = "geckodriver.exe"
SELENIUM_DRIVER_ARGUMENTS = ['-headless']

DOWNLOAD_DELAY = 5
