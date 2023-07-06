import json

# Carga los datos del archivo JSON
with open("ComfortZone.json") as f:
    data = json.load(f)

# Modifica el campo relevancia
for i, producto in enumerate(data["Productos"], 1):
    producto["relevancia"] = i

# Guarda los datos modificados en el archivo JSON
with open("data.json", "w") as f:
    json.dump(data, f)