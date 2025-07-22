import pandas
from sklearn import linear_model

df = pandas.read_csv("C:\Repo\python\ml-w3\data.csv")

X = df[['Weight', 'Volume']]
y = df['CO2']

model = linear_model.LinearRegression()
X = X.values # conversion of X  into array
model.fit(X, y)

#predict the CO2 emission of a car where the weight is 2300kg, and the volume is 1300cm3:
predictedCO2 = model.predict([[2300, 1300]])

print(predictedCO2)