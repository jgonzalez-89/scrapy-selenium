import json

# Carga los datos del archivo JSON
with open("ComfortZone.json") as f:
    data = json.load(f)

# Invierte la lista de productos para conservar el primer producto con cualquier ASIN duplicado
data['Productos'].reverse()

# Crea un diccionario donde cada producto es una entrada y el ASIN es la clave
productos_dict = {producto['ASIN']: producto for producto in data['Productos']}

# Convierte el diccionario de vuelta a una lista para eliminar los duplicados
# Y vuelve a invertir la lista para restaurar el orden original
data['Productos'] = list(productos_dict.values())[::-1]

# Guarda los datos modificados en el archivo JSON
with open("data.json", "w") as f:
    json.dump(data, f)