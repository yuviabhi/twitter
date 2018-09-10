'''

Trying out SVM and other classifiers

'''


import pandas as pd
x = pd.read_csv('feature_vector_output.csv')
y = pd.read_csv('flood-kolkata-20170725_labelled.csv')

>>> x.head()
>>> x[0:100]

from sklearn.linear_model import SGDClassifier

model = SGDClassifier()
model.fit(x[0:70],y[0:70])


SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
       eta0=0.0, fit_intercept=True, l1_ratio=0.15,
       learning_rate='optimal', loss='hinge', n_iter=5, n_jobs=1,
       penalty='l2', power_t=0.5, random_state=None, shuffle=True,
       verbose=0, warm_start=False)


>>> model.predict(x[70:100])

array([0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
       0, 1, 0, 0, 1, 0, 0])


>>> import sklearn.metrics
>>> y_pred = model.predict(x[70:100])
>>> sklearn.metrics.accuracy_score(y[70:100],y_pred)
0.26666666666666666



>>> from sklearn.svm import SVC
>>> model = SVC()
>>> model.fit(x[0:70],y[0:70])
SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
  decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
  max_iter=-1, probability=False, random_state=None, shrinking=True,
  tol=0.001, verbose=False)

>>> y_pred = model.predict(x[70:100])
>>> sklearn.metrics.accuracy_score(y[70:100],y_pred)
0.90000000000000002


>>> import sklearn.model_selection
>>> cv_score = sklearn.model_selection.cross_val_score(model,x[0:100],y,cv=10)

>>> y.size
100

>>> x.size
5072
>>> X= x[0:100]

>>> X.head()
    a    b
0  20   34
1  24  126
2  16   -1
3  27   66
4  10   -1

>>> X.size
200


>>> import numpy as np
>>> X = np.array(X)
>>> y = np.array(y)
>>> X.shape
(100, 2)
>>> y.shape
(100, 1)
>>> y = np.ndarray.flatten(y)
>>> cv_score = sklearn.model_selection.cross_val_score(model,X,y)
>>> y.shape
(100,)
>>> print cv_score
[ 0.88235294  0.87878788  0.87878788]
>>> cv_score = sklearn.model_selection.cross_val_score(model,X,y, cv=10)
>>> print cv_score
[ 0.81818182  0.81818182  0.9         0.9         0.9         0.9         0.9
  0.9         0.88888889  0.88888889]

