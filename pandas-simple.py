import pandas as pd

dataset = {
    'coches':  ["Volvo", "Mazda", "Ford"],
    'precios': ["10.000", "15.000", "20.000"]
}

variable = pd.DataFrame(dataset)

print(variable)

#--------------------------------------------------------------

a = [1, 7, 2]

myvar = pd.Series(a, index = ["x", "y", "z"])

print(myvar)

#--------------------------------------------------------------

calories = {"day1": 420, "day2": 380, "day3": 390}

myvar2 = pd.Series(calories)

print(myvar2)

#--------------------------------------------------------------

calories2 = {"day1": 420, "day2": 380, "day3": 390}

myvar3 = pd.Series(calories2, index = ["day1", "day2"])

print(myvar3)

#--------------------------------------------------------------

data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}

myvar4 = pd.DataFrame(data, index = ["day1", "day2", "day3"])

print(myvar4)