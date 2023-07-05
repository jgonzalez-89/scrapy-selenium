import os
import json
from datetime import datetime

# Cambia esto a tu directorio actual
directorio = '.'

def transforma_json(archivo):
    with open(os.path.join(directorio, archivo), 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_data = []
    
    for item in data:
        new_item = {}
        new_item['fecha'] = datetime.strptime(item['fecha'], "%d-%m-%Y").strftime("%Y-%m-%d")
        new_item['nombre'] = item['nombre']
        new_item['ASIN'] = item['ASIN']
        
        historicos = {}
        for vendedor, precio in zip(item['vendedores'], item['precios']):
            if vendedor not in historicos:
                historicos[vendedor] = []
            historicos[vendedor].append({"fecha": new_item['fecha'], "precio": precio})
        
        new_item['historicos'] = historicos
        new_data.append(new_item)

    fecha_nuevo_archivo = new_item['fecha']
    with open(os.path.join(directorio, fecha_nuevo_archivo + '.json'), 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4)

# Procesa todos los archivos JSON en el directorio
for archivo in os.listdir(directorio):
    if archivo.endswith('.json'):
        transforma_json(archivo)