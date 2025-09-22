from sklearn import datasets
from sklearn.linear_model import LogisticRegression

iris = datasets.load_iris()

X = iris['data']
y = iris['target']

logit = LogisticRegression(max_iter = 10000)

print(logit.fit(X,y))
# With the default setting of C = 1, we achieved a score of 0.973.
print(logit.score(X,y))

#Implementing Grid Search
#We will follow the same steps of before except this time we will set a range of values for C.
#Knowing which values to set for the searched parameters will take a combination of domain knowledge and practice.

C = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]

scores = []

for choice in C:
  logit.set_params(C=choice)
  logit.fit(X, y)
  scores.append(logit.score(X, y))

print(scores)