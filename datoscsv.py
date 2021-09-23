import pandas as pd

df = pd.read_csv('dirtydata.csv')

df.dropna(inplace = True)                  # Remueve filas nulas
df.dropna(subset=['Date'], inplace = True) # Corrige formato de fecha
df.drop_duplicates(inplace = True)         # Remueve duplicados

df['Date'] = pd.to_datetime(df['Date'])

print(df.to_string())

x = df["Calories"].median()

print(x)