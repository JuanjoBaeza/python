import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

df = pd.read_csv("C:\Repo\python\ml-w3\data-tree.csv")

d = {'UK': 0, 'USA': 1, 'N': 2}
df['Nationality'] = df['Nationality'].map(d)
d = {'YES': 1, 'NO': 0}
df['Go'] = df['Go'].map(d)

features = ['Age', 'Experience', 'Rank', 'Nationality']

X = df[features]
y = df['Go']

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)

tree.plot_tree(dtree, feature_names=features)
plt.show()

#Example: Should I go see a show starring a 40 years old American comedian, 
#with 10 years of experience, and a comedy ranking of 7?

sample = pd.DataFrame([[40, 10, 7, 1]], columns=features)
print("Predicción:", dtree.predict(sample)[0])