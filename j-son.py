import json
 
# Opening JSON file
file = open('datos/data.json',)
 
# returns JSON object as
# a dictionary
data = json.load(file)
 
print(data["orders"][1]["toppings"])
 
# Closing file
file.close()