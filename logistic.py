# see http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression.decision_function
#     http://scikit-learn.org/stable/auto_examples/linear_model/plot_iris_logistic.html#sphx-glr-auto-examples-linear-model-plot-iris-logistic-py
#     https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.metric import classification_report
import statsmodels.api as sm

data = pd.read_csv('books.csv')

y = data[ 'author' ]
# cols = all features except author
X = data[ cols ]


''' how is this api different from sklearn? '''
logit_model = sm.Logit( y, X )
result = logit_model.fit()
print(result.summary())


# standard percentage split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

# 10-fold cross validation
kfold = model_selection.KFold(n_splits=10, random_state=7)
modelCV = LogisticRegression()
scoring = 'accuracy'
results = model.selection.cross_val_score(modelCV, X_train, y_train, cv=kfold, scoring=scoring)
print("10-fold cross validation average accuracy: %.3f".format(results.mean()))

print(classification_report(y_test, y_pred))
