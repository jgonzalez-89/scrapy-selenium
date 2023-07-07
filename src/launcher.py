import os
import sys
import subprocess
import datetime
import requests
import logging
import shutil

logging.basicConfig(
    filename="launcher.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def run_scraper(scraper_name, json_file_path):
    
    # Elimina el archivo si existe antes de empezar el scraper
    if os.path.isfile(json_file_path):
        os.remove(json_file_path)

    project_path = os.path.dirname(os.path.abspath(__file__))
    scraper_path = os.path.join(project_path, f"selenium_{scraper_name}")
    os.chdir(scraper_path)
    sys.path.append(scraper_path)
    try:
        cmd = f"scrapy crawl {scraper_name}"
        subprocess.run(cmd, shell=True, check=True)
        logging.info(f"Scraper {scraper_name} ejecutado exitosamente")
    except Exception as e:
        logging.error(f"Error al ejecutar el scraper {scraper_name}: {e}")
        raise
    finally:
        os.chdir(project_path)
        return scraper_path


def send_file_to_api(file_path, api_url):
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(api_url, files=files)
            response.raise_for_status()
            logging.info(f"Archivo {file_path} enviado a la API exitosamente")
        return response
    except Exception as e:
        logging.error(f"Error al enviar el archivo {file_path} a la API: {e}")
        raise


def main():
    try:
        date_string = datetime.datetime.now().strftime("%Y-%m-%d")
        json_file_name = f"{date_string}.json"

        # Scraper de Amazon
        scraper_path = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(scraper_path, f"selenium_amazon", json_file_name)
        run_scraper("amazon", json_file_path)

        api_url_amazon = "http://127.0.0.1:8000/amazon/file/"
        send_file_to_api(json_file_path, api_url_amazon)
        shutil.move(json_file_path, f"./amazon_logs/{json_file_name}")

        # Scraper de Google
        scraper_path = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(scraper_path, f"selenium_google", json_file_name)
        run_scraper("google", json_file_path)

        api_url_google = "http://127.0.0.1:8000/google/file/"
        send_file_to_api(json_file_path, api_url_google)
        shutil.move(json_file_path, f"./google_logs/{json_file_name}")

    except Exception as e:
        logging.error(f"Error en el proceso principal: {e}")


if __name__ == "__main__":
    main()

# input("Press enter to exit ;")


# def run_scraper(scraper_name):
#     project_path = os.path.dirname(os.path.abspath(__file__))
#     scraper_path = os.path.join(project_path, f"selenium_{scraper_name}")
#     os.chdir(scraper_path)
#     sys.path.append(scraper_path)
#     try:
#         cmd = f"scrapy crawl {scraper_name}"
#         subprocess.run(cmd, shell=True, check=True)
#         logging.info(f"Scraper {scraper_name} ejecutado exitosamente")
#     except Exception as e:
#         logging.error(f"Error al ejecutar el scraper {scraper_name}: {e}")
#         raise
#     finally:
#         os.chdir(project_path)  # Regresar al directorio del proyecto después de ejecutar el scraper


# def send_file_to_api(file_path, api_url):
#     try:
#         with open(file_path, "rb") as f:
#             files = {"file": f}
#             response = requests.post(api_url, files=files)
#             response.raise_for_status()
#             logging.info(f"Archivo {file_path} enviado a la API exitosamente")
#         return response
#     except Exception as e:
#         logging.error(f"Error al enviar el archivo {file_path} a la API: {e}")
#         raise


# def main():
#     try:
#         date_string = datetime.datetime.now().strftime("%Y-%m-%d")
#         json_file = f"{date_string}.json"

#         run_scraper('amazon')
#         api_url_amazon = "http://127.0.0.1:8000/amazon/file/"
#         send_file_to_api(json_file, api_url_amazon)
#         shutil.move(json_file, f"./amazon_logs/{json_file}")

#         run_scraper('google')
#         api_url_google = "http://127.0.0.1:8000/google/file/"
#         send_file_to_api(json_file, api_url_google)
#         shutil.move(json_file, f"./google_logs/{json_file}")

#     except Exception as e:
#         logging.error(f"Error en el proceso principal: {e}")


# if __name__ == "__main__":
#     main()
