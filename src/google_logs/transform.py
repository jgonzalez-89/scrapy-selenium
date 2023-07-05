import os
import json
import random

def modify_json(path):
    # List all files in the directory
    for filename in os.listdir(path):
        # Check if file is .json
        if filename.endswith(".json"):
            # Open the json file
            with open(os.path.join(path, filename), 'r') as f:
                data = json.load(f)

            # Extract the date from the filename
            date = filename.replace(".json", "")

            # Modify the 'fecha' field and prices
            for item in data:
                item['fecha'] = date
                
                for i in range(len(item['precios'])):
                    # Generate a random percentage between -20% and +20%
                    percentage = random.uniform(-0.2, 0.2)

                    # Apply the percentage to the price and round to 2 decimals
                    item['precios'][i] = round(item['precios'][i] + item['precios'][i] * percentage, 2)

            # Write back to the file
            with open(os.path.join(path, filename), 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

# Use the function on your directory
modify_json(".")  # "." represents the current directory


