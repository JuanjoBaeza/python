import pandas as pd
import matplotlib.pyplot as pl

df = pd.read_csv('data.csv')

x = df.corr()
print (x)

df.plot()
pl.show()

df.plot(kind = 'scatter', x = 'Duration', y = 'Calories')
pl.show()

df.plot(kind = 'hist')
pl.show() 