import os
import sys
import subprocess
import datetime
import json
import requests
import logging
import psycopg2
import uuid


logging.basicConfig(
    filename="launcher.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_asins(user_id):
    try:
        connection = psycopg2.connect(
            user="database_bm6b_user",
            password="GFzUrYSTqU239m5pYQ9QiVHZKJl2MA0D",
            host="dpg-chaddcqk728r881d0t0g-a.frankfurt-postgres.render.com",
            port="5432",
            database="database_bm6b",
        )
        cursor = connection.cursor()

        query = f'SELECT "ASIN" FROM user_product_list WHERE user_id = {user_id};'
        cursor.execute(query)
        asins = cursor.fetchall()  # devuelve una lista de tuplas

        # transformar la lista de tuplas a una lista de strings
        asin_list = [asin[0] for asin in asins]
        print(asin_list)

        return asin_list

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def run_scraper(user_id):
    project_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_path)
    sys.path.append(project_path)
    try:
        asin_list = get_asins(user_id)
        asin_string = ",".join(asin_list)
        uuid_random = str(uuid.uuid4())
        date_string = datetime.datetime.now().strftime("%Y-%m-%d")
        output_file = f"{date_string}-{uuid_random}.json"
        cmd = f"scrapy crawl amazon -o {output_file} -a asin_list={asin_string}"
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


def main():
    try:
        user_id = 1  # o el ID del usuario que quieras
        json_file = run_scraper(user_id)
        process_json_file(json_file)

        api_url = f"http://127.0.0.1:5000/user/{user_id}/add_product"
        response = send_file_to_api("send.json", api_url)

        os.remove("send.json")
        logging.info("Archivo send.json eliminado")
    except Exception as e:
        logging.error(f"Error en el proceso principal: {e}")


if __name__ == "__main__":
    main()