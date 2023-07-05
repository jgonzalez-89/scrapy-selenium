import json

# Carga los datos del archivo JSON
with open("Data_update.json") as f:
    data = json.load(f)

# Modifica el campo relevancia
for i, producto in enumerate(data["Productos"], 1):
    producto["relevancia"] = i

# Guarda los datos modificados en el archivo JSON
with open("Davines_update.json", "w") as f:
    json.dump(data, f)