import pandas as pd 
import numpy as np

# Create Series from array
data = np.array(['python','php','java'])
series = pd.Series(data)
print (series,"\n")

# Create a Dict from a input
data = {'Courses' :"pandas", 'Fees' : 20000, 'Duration' : "30days"}
s2 = pd.Series(data)
print (s2, "\n")

#Creating DataFrame from List
data = ['python','php','java']
s2 = pd.Series(data, index=['r1', 'r2','r3'])
print(s2,"\n")