import numpy as np
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import confusion_matrix
import codes.databaseHandler as databaseHandler




dh=databaseHandler.databaseHandler()
#
# def makeRequestNumberic(string):
#     k = [0 for i in range(255)]
#     for char in string:
#         k[ord(char)] += 1
#     return k

def makeRequestSequenceOfChars(string):
    k=[]
    for char in string:
        k.append(ord(char))
    length=len(k)
    t=[0 for i in range(256-length)] # fill the rest with 0, so as they will have same length
    return k+t
#Prepairing data
data=dh.selectAllRecords()
X=[]
y=[]
for element in data:
    X.append(makeRequestSequenceOfChars(element.request_url))
    y.append(element.request_type)

X=np.array(X)
# X = np.array([makeRequestNumberic(i) for i in string])
# X = np.array([makeRequestSequenceOfChars(i) for i in string])

labelencoder_y=LabelEncoder()
y=labelencoder_y.fit_transform(y)

kf = KFold(n_splits=5)


# create classifier
from sklearn.ensemble import RandomForestClassifier

for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    classifier = RandomForestClassifier(n_estimators=5, criterion='entropy')
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    cm=confusion_matrix(y_pred=y_pred,y_true=y_test)
    print(cm)