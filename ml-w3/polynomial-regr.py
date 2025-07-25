import matplotlib.pyplot as plt
from scipy import stats
import numpy

x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
y = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]


slope, intercept, r, p, std_err = stats.linregress(x, y)

#Esto muestra el coeficiente de regresion linear, debe existir una correlacion entre x e y.
print(r)

mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))

myline = numpy.linspace(1, 22, 100)

plt.scatter(x, y)
plt.plot(myline, mymodel(myline))
plt.show()