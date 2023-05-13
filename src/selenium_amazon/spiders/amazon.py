import scrapy
import re
import random
import time
from scrapy.spiders import Spider
from scrapy import Request
import datetime
from scrapy_selenium import SeleniumRequest
from user_agent import generate_user_agent
import logging

logging.getLogger("protego").setLevel(logging.WARNING)
logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(
    logging.WARNING
)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

# scrapy crawl product_scraper -a asin=B01DS0HUK6 -o 04-05-2023.json


class AmazonSpider(scrapy.Spider):
    name = "amazon"

    def __init__(self, asin=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if asin:
            self.asin = asin.split(",")
        else:
            self.asin = [
                "B00ZPQ129C",
                "B06ZZ6CDY1",
                "B07RRBZF7T",
                "B00GCCQ3DI",
                "B011DCMQZA",
                "B00GTW4S3S",
                "B0073FD66A",
                "B0073FO9AM",
                "B07ZJ82DFL",
                "B08SXSWC7Y",
                "B06XSF4R1X",
                "B07ZL56NS7",
                "B00GTW4QQ2",
                "B00U1JHWR4",
                "B0813DB98Y",
                "B01MSA66C8",
                "B01MUI8JBV",
                "B06XDGDTM9",
                "B08MFP4KHH",
                "B01NBXIKIL",
                "B06Y3NHWVG",
                "B01N36O3RT",
                "B07BZDZ3JM",
                "B077NGWYRX",
                "B07BZF3HM7",
                "B08JL2QNCC",
                "B07KJB395Z",
                "B075WD97B2",
                "B06XDD6W7T",
                "B08JL451SN"
            ]

    def start_requests(self):
        for asin in self.asin:
            url = f"https://www.amazon.es/gp/offer-listing/{asin}"
            print(f"URL: {url}")  # Agrega esta línea para depurar
            headers = {"User-Agent": generate_user_agent()}
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                headers=headers,
                meta={
                    "handle_httpstatus_list": [503],
                    "dont_redirect": True,
                    "original_url": url,
                },
            )

    def parse(self, response):
        try:
            codigo_ASIN = self.extract_codigo(response.url)
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = self.extract_nombre(response)
            imagen = self.extract_imagen(response)
            numero_EAN = self.extract_EAN(response)

            offers = response.xpath("//*[@id='aod-pinned-offer']|//*[@id='aod-offer']")
            vendedores = []
            precios = []

            for offer in offers:
                price = offer.xpath(
                    ".//span[contains(@class, 'a-price')]/span[contains(@class, 'a-offscreen')]/text()"
                ).get()
                vendor = offer.xpath(
                    ".//*[@id='aod-offer-soldBy']/div/div/div[2]/a/text()"
                ).get()

                if price:
                    price = float(price.replace("€", "").replace(",", "."))
                    precios.append(price)

                if vendor:
                    vendedores.append(vendor.strip())

            if not vendedores or not precios:
                raise Exception("No se encontraron vendedores o precios")
            else:
                yield {
                    "fecha": fecha,
                    "imagen": imagen,
                    "nombre": nombre,
                    "vendedores": vendedores,
                    "precios": precios,
                    "ASIN": codigo_ASIN,
                    "EAN": numero_EAN,
                }
                time.sleep(random.uniform(1, 3))

        except Exception as e:
            retry_times = response.meta.get("retry_times", 0) + 1

            if retry_times <= 10:  # Puedes ajustar el número máximo de intentos
                self.logger.info(
                    f"Reintentando {response.meta['original_url']} (intento {retry_times}) - Error: {str(e)}"
                )
                time.sleep(
                    random.uniform(1, 3)
                )  # Agrega tiempo de espera entre intentos
                headers = {"User-Agent": generate_user_agent()}  # Agrega encabezados
                yield SeleniumRequest(
                    url=response.meta["original_url"],
                    callback=self.parse,
                    headers=headers,
                    meta={
                        "handle_httpstatus_list": [503],
                        "dont_redirect": True,
                        "retry_times": retry_times,
                        "original_url": response.meta["original_url"],
                    },
                    dont_filter=True,  # Agrega esta línea
                )
                return

    @staticmethod
    def extract_precio(response):
        precio_str = response.xpath(
            ".//span[contains(@class, 'a-price-whole')]/text()"
        ).get()
        if precio_str is not None:
            precio_str = precio_str.strip()
            return float(precio_str.replace(",", "."))
        return None

    @staticmethod
    def extract_nombre(response):
        nombre = response.xpath("//*[@id='productTitle']/text()").get()
        if nombre:
            return nombre.replace('"', "").lower().strip()
        return None

    @staticmethod
    def extract_EAN(response):
        span_elements = response.xpath("//span/text()").getall()
        numero_modelo_regex = r"\b\d{13}\b"
        for element in span_elements:
            match = re.search(numero_modelo_regex, element)
            if match:
                return match.group(0)
        return None

    @staticmethod
    def extract_imagen(response):
        return response.xpath("//*[@id='landingImage']/@src").get()

    @staticmethod
    def extract_codigo(url):
        codigo_regex = r"\b[B0-9][A-Z0-9]{9}\b"
        match = re.search(codigo_regex, url)
        if match:
            return match.group(0)
        return None

    # @staticmethod
    # def extract_codigo(response):
    #     span_elements = response.xpath("//span/text()").getall()
    #     codigo_regex = r"\b[A-Z0-9]{10}\b"
    #     for element in span_elements:
    #         match = re.search(codigo_regex, element)
    #         if match:
    #             return match.group(0)
    #     return None
