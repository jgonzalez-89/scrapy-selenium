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

# scrapy crawl product_scraper -a gsi=B01DS0HUK6 -o 04-05-2023.json


class TestingSpider(scrapy.Spider):
    name = "testing"

    def __init__(self, code=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if code:
            self.code = code.split(",")
        else:
            self.code = [
                "B01N36O3RT",
                "B085GK4LQF",
                "B07KJ8MPD1",
                "B07C7KCF4W",
                "B01N5S2BHO",
                "B07BZDZ3JM",
                "B015UDH09A",
                "B015UCTS5U",
                "B07C25PY16",
                "B01N9UH4T9",
                "B01DRZEK96",
                "B07Z1BWSYX",
                "B015UD2POA",
                "B075WD97B2",
                "B06Y3NHWVG",
                "B01NB0TI00",
                "B01MSA66C8",
                "B07BZM3HQH",
                "STRATEGIST",
                "B06XDGM9HL",
                "B01NAVYVLG",
                "B0190MZQ34",
                "B01MUI8JBV",
                "B015UD5JLG",
                "B01MYFU663",
                "B01ND3RNF9",
                "B01NC23R9N",
                "B077NF3R4W",
                "B06XDGDTM9",
                "B01N7UYUVY",
                "B01NBXIKIL",
                "B074Y3DQ47",
                "B077NGWYRX",
                "B01JTHDLTQ",
                "B06XD65SNZ",
                "B07L5Q9F49",
                "B07KJBL9RK",
                "B07KK15DY1",
                "B07KJB395Z",
                "B07KJD3N8M",
                "B01N36NQVJ",
            ]

    def start_requests(self):
        for code in self.code:
            # url = f"https://www.google.es/shopping/product/{code}/offers?hl=es&"
            url = f"https://www.amazon.es/dp/{code}"

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
                    "code": code,  # Agrega el código GSI a los metadatos
                },
            )

    def parse(self, response):
        try:
            # Extraer la información usando las funciones definidas
            codigo_asin = response.meta[
                "code"
            ]  # Obtiene el código GSI de los metadatos
            # fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = self.extract_nombre(response)
            imagen = self.extract_imagen(response)
            precio = self.extract_precio(response)
            # vendedores = self.extract_vendedor(response)

            # if nombre is None or imagen is None or precio is None:
            #     raise Exception("No se pudo extraer toda la información necesaria")

            yield {
                "EAN": 1,
                "GSI": 2,
                # "fecha": fecha,
                "nombre": nombre,
                "distribuidor": "ComfortZone",
                "precio": precio,
                "ASIN": codigo_asin,
                "imagen": imagen,
                "relevancia": 0,
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

    # @staticmethod
    # def extract_precio(response):
    #     precios_str = response.xpath("//div[@class='drzWO']/text()").getall()
    #     precios = []
    #     for precio_str in precios_str:
    #         # Aquí, debemos quitar el símbolo del euro y reemplazar la coma con un punto
    #         precio_str = (
    #             precio_str.replace(",", ".")
    #             .replace("&nbsp;€", "")
    #             .replace("€", "")
    #             .strip()
    #         )
    #         try:
    #             precios.append(float(precio_str))
    #         except ValueError:
    #             continue  # Si no podemos convertir a float, saltamos el precio
    #     return precios
    @staticmethod
    def extract_precio(response):
        precio_str = response.xpath(
            ".//span[contains(@class, 'a-price-whole')]/text()"
        ).get()
        if precio_str is not None:
            precio_str = precio_str.strip()
            return float(precio_str.replace(",", "."))
        return None

    # @staticmethod
    # def extract_nombre(response):
    #     nombre = response.xpath(
    #         "//a[@class='BvQan sh-t__title sh-t__title-pdp translate-content']/text()"
    #     ).get()
    #     if nombre:
    #         return nombre.replace('"', "").lower().strip()
    #     return None
    @staticmethod
    def extract_nombre(response):
        nombre = response.xpath("//*[@id='productTitle']/text()").get()
        if nombre:
            return nombre.replace('"', "").lower().strip()
        return None

    # @staticmethod
    # def extract_imagen(response):
    #     return response.xpath("//img[@class='r4m4nf']/@src").get()
    @staticmethod
    def extract_imagen(response):
        return response.xpath("//*[@id='landingImage']/@src").get()

    # @staticmethod
    # def extract_codigo(url):
    #     codigo_regex = r"\b\d{20}\b"  # busca una secuencia de 20 dígitos
    #     match = re.search(codigo_regex, url)
    #     if match:
    #         return match.group(0)
    #     return None

    # @staticmethod
    # def extract_vendedor(response):
    #     vendedores = response.xpath("//a[@class='b5ycib shntl']/text()").getall()
    #     vendedores = [v.strip() for v in vendedores]
    #     return vendedores

    # @staticmethod
    # def extract_precio(response):
    #     precio_str = response.xpath(
    #         ".//span[contains(@class, 'a-price-whole')]/text()"
    #     ).get()
    #     if precio_str is not None:
    #         precio_str = precio_str.strip()
    #         return float(precio_str.replace(",", "."))
    #     return None

    # @staticmethod
    # def extract_nombre(response):
    #     nombre = response.xpath("//*[@id='productTitle']/text()").get()
    #     if nombre:
    #         return nombre.replace('"', "").lower().strip()
    #     return None

    # @staticmethod
    # def extract_EAN(response):
    #     span_elements = response.xpath("//span/text()").getall()
    #     numero_modelo_regex = r"\b\d{13}\b"
    #     for element in span_elements:
    #         match = re.search(numero_modelo_regex, element)
    #         if match:
    #             return match.group(0)
    #     return None

    # @staticmethod
    # def extract_imagen(response):
    #     return response.xpath("//*[@id='landingImage']/@src").get()

    # @staticmethod
    # def extract_codigo(url):
    #     codigo_regex = r"\b[B0-9][A-Z0-9]{9}\b"
    #     match = re.search(codigo_regex, url)
    #     if match:
    #         return match.group(0)
    #     return None

    # "B0073FO9AM",
    # "B00OKME7S0",
    # "B00HUEGDZU",
    # "B00GB8V338",
    # "B07661NQDH",
    # "B073WF21FL",
    # "B07BNRR82Z",
    # "B007XNNF72",
    # "B00OKS2H5Y",
    # "B076QFZPCS",
    # "B00RYOH38M",
    # "B006IUYSZO",
    # "B00OOVQVGS",
    # "B07D1RG262",
    # "B00GB8OJA2",
    # "B076QFV8CW",
    # "B0162EDN4W",
    # "B00OOVAJV6",
    # "B00GCCH6AM",
    # "B07CZ6DMK4",
    # "B00GB8RJ40",
    # "B00QFKRQO2",
    # "B0130KXHW4",
    # "B0725Q5H11",
    # "B074SHC7XG",
    # "B0073FZHMG",
    # "B01M5JMMZA",
    # "B07D1DJ8TH",
    # "B00VO6BX6E",
    # "B01CUYO004",
    # "B00VO6BJ40",
    # "B073P2JXJ6",
    # "B01LY8TERO",
    # "B00QFL8G9U",
    # "B008AW6L5S",
    # "B00CGPMFA0",
    # "B00CGPJDCS",
    # "B07D1S8MV8",
    # "B075JM91SV",
    # "B00VDW61LQ",
    # "B00GB8T5P6",
    # "B0774H86RS",
    # "B0087CW9G6",
    # "B007804K1U",
    # "B00514HDDW",
    # "B00VO6BMSS",
    # "B08BV2JHQ5",
    # "B00VO6BQ98",
    # "B00WT4CKH6",
    # "B00R13JF82",
    # "B00VO6CERG",
    # "B00OOU62GI",
    # "B01LEJKG36",
    # "B0073G6B70",
    # "B005CKGO7Q",
    # "B0087CWAJC",
    # "B09LM698WG",
    # "B01DF7WCP0",
    # "B07C54JJRX",
    # "B07D8RKS7Y",
    # "B015JWDUUA",
    # "B07DRJ7KSM",
    # "B075QLWXGP",
    # "B0165H0MRC",
    # "B0746GSVF6",
