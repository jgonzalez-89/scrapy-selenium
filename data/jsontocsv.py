import json
import csv

# Cargar el archivo json
with open('Davines.json', 'r') as f:
    data = json.load(f)["Productos"]

# Nombres de las columnas
fields = ["EAN", "GSI", "nombre", "distribuidor", "precio", "ASIN", "imagen", "relevancia"]

# Escribir los datos del json a un archivo csv
with open('Davines.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for item in data:
        writer.writerow(item)
