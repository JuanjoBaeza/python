thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x) 

car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
    }

x = car.keys()

print(x) #before the change

car["color"] = "white"

print(x) #after the change 