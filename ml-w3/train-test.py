import numpy
import matplotlib.pyplot as plt
numpy.random.seed(2)
from sklearn.metrics import r2_score

x = numpy.random.normal(3, 1, 100)
y = numpy.random.normal(150, 40, 100) / x

train_x = x[:80]
train_y = y[:80]

test_x = x[80:]
test_y = y[80:]

mymodel = numpy.poly1d(numpy.polyfit(train_x, train_y, 4))
myline  = numpy.linspace(0, 6, 100)
r2 = r2_score(test_y, mymodel(test_x))

#Remember R2, also known as R-squared?
#It measures the relationship between the x axis and the y axis, and the value ranges 
#from 0 to 1, where 0 means no relationship, and 1 means totally related.
print(r2)

#How much money will a buying customer spend, if she or he stays in the shop for 5min?
print(mymodel(5))

plt.scatter(train_x, train_y)
plt.plot(myline, mymodel(myline))
plt.show()