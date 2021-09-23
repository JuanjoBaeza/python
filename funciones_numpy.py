import numpy as p
import click
from scipy import stats

click.clear()

vel = [4,56,77,85,33,48,127,89,142]

x = p.median(vel)   # Media
y = p.mean(vel)     # Mediana
z = stats.mode(vel) # Moda
a = p.std(vel)      # Desviacion típica
b = p.var(vel)      # Varianza

x = "%.2f" % x
y = "%.2f" % y
a = "%.2f" % a
b = "%.2f" % b

print(x, y , z, a, b)