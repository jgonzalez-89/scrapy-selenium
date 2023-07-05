import json
import requests

# Carga los datos del archivo JSON
with open("Davines.json") as f:
    data = json.load(f)

# URL del endpoint
url = "http://127.0.0.1:8000/davines/crear/"

# Token de autenticación
auth_token = "ccf17c0cf75187f21cd6b17b98aa19b4bf1031e5"

# Cabeceras HTTP
headers = {
    "auth_token": auth_token,
}

# Itera sobre los productos y realiza una solicitud POST para cada uno
for producto in data["Productos"]:
    # Realiza una solicitud POST
    response = requests.post(url, json=producto, headers=headers)
    
    # Si la solicitud falla, imprime la respuesta
    if response.status_code != 200:
        print(f"Failed to post product {producto['ASIN']}: {response.text}")
