import os
import sys
import subprocess
import datetime
import json
import requests
import logging

logging.basicConfig(
    filename="launcher.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run_scraper():
    project_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_path)
    sys.path.append(project_path)
    try:
        date_string = datetime.datetime.now().strftime("%Y-%m-%d")
        output_file = f"{date_string}.json"
        cmd = f"/usr/local/bin/scrapy crawl amazon -o {output_file}"
        # cmd = f"scrapy crawl amazon -o {output_file}"
        subprocess.run(cmd, shell=True, check=True)
        logging.info("Scraper ejecutado exitosamente")
        return output_file
    except Exception as e:
        logging.error(f"Error al ejecutar el scraper: {e}")
        raise


def transform_data(input_data):
    transformed_data = []

    for product in input_data:
        transformed_product = {
            "fecha": product["fecha"],
            "imagen": product["imagen"],
            "nombre": product["nombre"],
            "ASIN": product["ASIN"],
            "EAN": product["EAN"],
            "historicos": {},
        }

        for vendedor, precio in zip(product["vendedores"], product["precios"]):
            if vendedor not in transformed_product["historicos"]:
                transformed_product["historicos"][vendedor] = []

            transformed_product["historicos"][vendedor].append(
                {"fecha": product["fecha"], "precio": precio}
            )

        transformed_data.append(transformed_product)

    return transformed_data


def process_json_file(json_file):
    with open(json_file, "r", encoding="utf-8") as input_file:
        input_data = json.load(input_file)

    transformed_data = transform_data(input_data)

    with open("send.json", "w", encoding="utf-8") as output_file:
        json.dump(transformed_data, output_file, indent=2, ensure_ascii=False)


def send_file_to_api(file_path, api_url):
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(api_url, files=files)
            response.raise_for_status()
            logging.info("Archivo enviado a la API exitosamente")
        return response
    except Exception as e:
        logging.error(f"Error al enviar el archivo a la API: {e}")
        raise


# def test_transform_data():
#     input_data = [
#         {
#             "fecha": "2023-05-05",
#             "imagen": "image_url",
#             "nombre": "product_name",
#             "ASIN": "ASIN123",
#             "EAN": "EAN123",
#             "vendedores": ["seller1", "seller2"],
#             "precios": [100, 200]
#         }
#     ]

#     expected_output = [
#         {
#             "fecha": "2023-05-05",
#             "imagen": "image_url",
#             "nombre": "product_name",
#             "ASIN": "ASIN123",
#             "EAN": "EAN123",
#             "historicos": {
#                 "seller1": [
#                     {
#                         "fecha": "2023-05-05",
#                         "precio": 100
#                     }
#                 ],
#                 "seller2": [
#                     {
#                         "fecha": "2023-05-05",
#                         "precio": 200
#                     }
#                 ]
#             }
#         }
#     ]

#     transformed_data = transform_data(input_data)
#     assert transformed_data == expected_output, f"Error: Resultado esperado {expected_output}, pero se obtuvo {transformed_data}"


def main():
    try:
        json_file = run_scraper()
        process_json_file(json_file)
        # test_transform_data()

        api_url = "http://127.0.0.1:5000/file"
        response = send_file_to_api("send.json", api_url)

        os.remove("send.json")
        logging.info("Archivo send.json eliminado")
    except Exception as e:
        logging.error(f"Error en el proceso principal: {e}")


if __name__ == "__main__":
    main()
