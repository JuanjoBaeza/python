import numpy
import matplotlib.pyplot as plt

x = numpy.random.uniform(0.0, 5.0, 100000)

print(x)         # Esto imprime los valores

plt.hist(x, 100) # Define el dibujo
plt.show()       # Muestra el dibujo