import os
import requests

def enviar_archivos_json(api_url, directorio):
    for filename in os.listdir(directorio):
        if filename.endswith(".json"):
            file_path = os.path.join(directorio, filename)
            with open(file_path, 'rb') as f:
                files = {'file': f}
                r = requests.post(api_url, files=files)
                print(f"Estado del envío del archivo {filename}: {r.status_code}")
                if r.status_code != 200:
                    print(f"Hubo un problema con el archivo {filename}: {r.text}")

api_url = "http://127.0.0.1:8000/google/file/"
directorio = "."  # Reemplaza con la ruta de tu directorio

enviar_archivos_json(api_url, directorio)
